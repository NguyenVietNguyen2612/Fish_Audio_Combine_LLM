import time
import requests
from typing import Generator, Dict, Any, Optional
import config

class FishAudioClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.FISH_AUDIO_API_KEY
        self.api_url = "https://api.fish.audio/v1/tts"

    def _get_api_key(self) -> str:
        key = self.api_key or config.FISH_AUDIO_API_KEY
        if not key:
            raise ValueError("FISH_AUDIO_API_KEY chưa được thiết lập. Vui lòng thêm vào file .env")
        return key

    def synthesize_stream(
        self,
        text: str,
        reference_id: Optional[str] = None,
        model: Optional[str] = None,
        latency: str = "balanced",
        audio_format: str = "mp3",
        speed: float = 1.0,
        volume: float = 0.0
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Gửi yêu cầu TTS tới Fish Audio Cloud API theo cơ chế streaming chunks.
        Hỗ trợ model free s2.1-pro-free hoặc s2.1-pro qua header.
        """
        start_time = time.perf_counter()
        target_model = model or config.DEFAULT_FISH_MODEL
        headers = {
            "Authorization": f"Bearer {self._get_api_key()}",
            "Content-Type": "application/json",
            "model": target_model
        }

        payload: Dict[str, Any] = {
            "text": text,
            "model": target_model,
            "format": audio_format,
            "latency": latency,
            "prosody": {
                "speed": speed,
                "volume": volume
            }
        }
        if reference_id and reference_id.strip():
            payload["reference_id"] = reference_id.strip()

        first_chunk_received = False
        ttfa_ms = None

        with requests.post(self.api_url, json=payload, headers=headers, stream=True) as response:
            if response.status_code != 200:
                error_detail = response.text
                raise RuntimeError(f"Fish Audio API lỗi ({response.status_code}): {error_detail}")

            for chunk in response.iter_content(chunk_size=4096):
                if not chunk:
                    continue

                current_time = time.perf_counter()
                elapsed_ms = (current_time - start_time) * 1000

                is_first = False
                if not first_chunk_received:
                    first_chunk_received = True
                    is_first = True
                    ttfa_ms = elapsed_ms

                yield {
                    "chunk": chunk,
                    "is_first": is_first,
                    "ttfa_ms": ttfa_ms,
                    "elapsed_ms": elapsed_ms
                }
