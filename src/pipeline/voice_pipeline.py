import time
import uuid
import re
from pathlib import Path
from typing import Dict, Any, Optional, Generator
import config
from src.llm.gemini_client import GeminiClient
from src.tts.fish_audio_client import FishAudioClient
from src.pipeline.chunker import StreamChunker
from src.utils.audio_utils import get_audio_duration_seconds

class VoicePipeline:
    def __init__(
        self,
        gemini_api_key: Optional[str] = None,
        fish_api_key: Optional[str] = None
    ):
        self.gemini_client = GeminiClient(api_key=gemini_api_key)
        self.fish_client = FishAudioClient(api_key=fish_api_key)

    def run(
        self,
        prompt: str,
        gemini_model: str = "gemini-3.1-flash-lite",
        voice_id: Optional[str] = None,
        fish_model: Optional[str] = None,
        language: str = "auto",
        emotion_tag: Optional[str] = None,
        system_instruction: Optional[str] = None,
        speed: float = 1.0,
        volume: float = 0.0
    ) -> Dict[str, Any]:
        """
        Chạy toàn bộ pipeline E2E đồng thời ghi nhận các chỉ số latency:
        - t0: Bắt đầu gửi request tới Gemini
        - t_first_token: Nhận token đầu tiên (LLM TTFT)
        - t_first_chunk: Chunker hoàn thành mệnh đề/câu đầu tiên
        - t_first_audio: Fish Audio trả về chunk audio đầu tiên (E2E First Audio Latency)
        """
        t0 = time.perf_counter()

        # Phân tích cảm xúc để tinh chỉnh ngữ điệu (Bracket Syntax + Prosody Tuning)
        bracket_tag = ""
        final_speed = speed
        final_volume = volume
        emo_lower = (emotion_tag or "").lower()

        if any(w in emo_lower for w in ["hào hứng", "vui", "excited", "happy", "joy"]):
            bracket_tag = "[laughing] [excited] "
            final_speed = 1.15 if speed == 1.0 else speed
            final_volume = 2.0 if volume == 0.0 else volume
        elif any(w in emo_lower for w in ["buồn", "sad", "trầm lắng", "khóc", "sorrow"]):
            bracket_tag = "[sigh] [sobbing] "
            final_speed = 0.85 if speed == 1.0 else speed
            final_volume = -3.0 if volume == 0.0 else volume
        elif any(w in emo_lower for w in ["tức giận", "angry", "căng thẳng", "furious"]):
            bracket_tag = "[angry] [screaming] "
            final_speed = 1.2 if speed == 1.0 else speed
            final_volume = 3.0 if volume == 0.0 else volume
        elif any(w in emo_lower for w in ["thì thầm", "whisper", "nhẹ nhàng", "khẽ"]):
            bracket_tag = "[whispering] "
            final_speed = 0.9 if speed == 1.0 else speed
            final_volume = -6.0 if volume == 0.0 else volume
        elif any(w in emo_lower for w in ["kịch tính", "hồi hộp", "dramatic", "khẩn cấp"]):
            bracket_tag = "[gasp] "
            final_speed = 1.1 if speed == 1.0 else speed
            final_volume = 1.5 if volume == 0.0 else volume

        # Chuẩn bị system instruction theo ngôn ngữ yêu cầu
        if language == "en":
            final_system_instruction = system_instruction or (
                "You are an expressive, natural voice assistant. You MUST reply in English. "
                "Keep your answer concise (1-2 short sentences), direct, and conversational. "
                "Do NOT use markdown symbols (no *, #, bullets, code blocks) so it can be spoken clearly."
            )
            if emotion_tag and emotion_tag.strip():
                final_system_instruction += (
                    f"\nDeliver with intense emotional expression: {emotion_tag.strip()}. "
                    f"Use appropriate emotional exclamations, interjections, or pacing to match the feeling."
                )
        elif language == "vi":
            final_system_instruction = system_instruction or (
                "Bạn là trợ lý ảo bằng giọng nói thông minh, tự nhiên. Bạn BẮT BUỘC phải trả lời bằng Tiếng Việt. "
                "Hãy trả lời súc tích, ngắn gọn (1-2 câu), tự nhiên, tuyệt đối không dùng các ký tự markdown "
                "(như *, #, gạch đầu dòng, mã code) để dễ dàng đọc thành tiếng."
            )
            if emotion_tag and emotion_tag.strip():
                final_system_instruction += (
                    f"\nHãy thể hiện cảm xúc rõ nét: {emotion_tag.strip()}. "
                    f"Sử dụng từ ngữ cảm thán, ngữ điệu phù hợp để giọng đọc truyền tải được cảm xúc này."
                )
        else:
            final_system_instruction = system_instruction or (
                "You are a smart, expressive voice assistant. Respond strictly in the same language as the user's prompt. "
                "Keep your answer concise (1-2 short sentences), natural, without markdown symbols (*, #, bullets) "
                "for seamless text-to-speech synthesis."
            )
            if emotion_tag and emotion_tag.strip():
                final_system_instruction += f"\nEmotional tone: {emotion_tag.strip()}."

        # 1. Khởi chạy LLM Stream và Chunker
        chunker = StreamChunker()
        full_text_list = []
        first_token_time = None
        first_chunk_ready_time = None
        first_chunk_text = None

        gemini_stream = self.gemini_client.generate_stream(
            prompt=prompt,
            model=gemini_model,
            system_instruction=final_system_instruction
        )

        for item in gemini_stream:
            token = item["token"]
            full_text_list.append(token)

            if item["is_first"] and first_token_time is None:
                first_token_time = time.perf_counter()

            # Đẩy vào chunker
            ready_chunks = chunker.process_token(token)
            if ready_chunks and first_chunk_ready_time is None:
                first_chunk_ready_time = time.perf_counter()
                first_chunk_text = ready_chunks[0]

        # Xả phần còn lại trong buffer
        flushed_chunks = chunker.flush()
        if flushed_chunks and first_chunk_ready_time is None:
            first_chunk_ready_time = time.perf_counter()
            first_chunk_text = flushed_chunks[0]

        llm_done_time = time.perf_counter()
        full_text = "".join(full_text_list).strip()

        if not full_text:
            raise RuntimeError("Gemini không sinh ra bất kỳ văn bản nào.")

        # 2. Gửi văn bản sang Fish Audio TTS
        # Để đo TTFA sớm nhất (First Audio Chunk):
        # Ta gửi toàn bộ câu hoàn chỉnh (hoặc câu đầu) vào Fish Audio Streaming
        tts_start_time = time.perf_counter()
        first_audio_time = None
        audio_chunks = []

        # Làm sạch ký tự markdown (*, #, _, `, ~) và bổ sung Emotion Bracket Tags
        clean_text_for_tts = re.sub(r'[*#_`~>]+', '', full_text).strip()
        clean_text_for_tts = re.sub(r'\s+', ' ', clean_text_for_tts)
        if bracket_tag and not clean_text_for_tts.startswith('['):
            clean_text_for_tts = f"{bracket_tag}{clean_text_for_tts}"

        tts_stream = self.fish_client.synthesize_stream(
            text=clean_text_for_tts or full_text,
            reference_id=voice_id,
            model=fish_model or config.DEFAULT_FISH_MODEL,
            latency=config.DEFAULT_FISH_LATENCY,
            audio_format="mp3",
            speed=final_speed,
            volume=final_volume
        )

        for audio_item in tts_stream:
            if audio_item["is_first"] and first_audio_time is None:
                first_audio_time = time.perf_counter()
            audio_chunks.append(audio_item["chunk"])

        tts_done_time = time.perf_counter()

        # 3. Lưu file MP3
        unique_id = f"{int(time.time())}_{uuid.uuid4().hex[:6]}"
        audio_filename = f"speech_{unique_id}.mp3"
        audio_filepath = config.AUDIO_OUTPUT_DIR / audio_filename

        with open(audio_filepath, "wb") as f:
            for chk in audio_chunks:
                f.write(chk)

        # 4. Tính toán các chỉ số
        audio_duration_s = get_audio_duration_seconds(audio_filepath)
        
        # Metrics
        llm_ttft_ms = (first_token_time - t0) * 1000 if first_token_time else 0.0
        first_chunk_latency_ms = (first_chunk_ready_time - t0) * 1000 if first_chunk_ready_time else 0.0
        tts_ttfa_ms = (first_audio_time - tts_start_time) * 1000 if first_audio_time else 0.0
        e2e_first_audio_ms = (first_audio_time - t0) * 1000 if first_audio_time else 0.0
        llm_total_ms = (llm_done_time - t0) * 1000
        tts_total_ms = (tts_done_time - tts_start_time) * 1000
        pipeline_total_ms = (tts_done_time - t0) * 1000
        
        rtf = round((tts_total_ms / 1000) / audio_duration_s, 3) if audio_duration_s > 0 else 0.0

        return {
            "text": full_text,
            "audio_filename": audio_filename,
            "audio_url": f"/api/audio/{audio_filename}",
            "metrics": {
                "llm_ttft_ms": round(llm_ttft_ms, 1),
                "first_chunk_latency_ms": round(first_chunk_latency_ms, 1),
                "tts_ttfa_ms": round(tts_ttfa_ms, 1),
                "e2e_first_audio_latency_ms": round(e2e_first_audio_ms, 1),
                "llm_total_ms": round(llm_total_ms, 1),
                "tts_total_ms": round(tts_total_ms, 1),
                "pipeline_total_ms": round(pipeline_total_ms, 1),
                "audio_duration_s": audio_duration_s,
                "rtf": rtf
            },
            "config": {
                "gemini_model": gemini_model,
                "voice_id": voice_id or "Mặc định (Default)",
                "emotion_tag": emotion_tag or "Không (None)",
                "speed": speed
            }
        }
