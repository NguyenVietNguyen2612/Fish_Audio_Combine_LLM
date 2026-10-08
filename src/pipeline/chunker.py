import re
from typing import Generator, List

class StreamChunker:
    """
    Bộ tách câu/mệnh đề thông minh từ luồng token của LLM.
    Giúp đẩy đoạn văn bản hoàn chỉnh sang TTS càng sớm càng tốt để tối ưu E2E Latency.
    """
    def __init__(self, min_clause_chars: int = 25, max_buffer_chars: int = 150):
        self.min_clause_chars = min_clause_chars
        self.max_buffer_chars = max_buffer_chars
        self.buffer = ""
        # Dấu kết thúc câu hoàn chỉnh
        self.sentence_delimiters = re.compile(r'([.!?\n]+)')
        # Dấu ngắt mệnh đề
        self.clause_delimiters = re.compile(r'([,;:—]+)')

    def process_token(self, token: str) -> List[str]:
        """
        Nhận token mới và trả về danh sách các câu/cụm câu sẵn sàng cho TTS nếu có.
        """
        self.buffer += token
        chunks_to_send: List[str] = []

        # Kiểm tra xem có dấu kết câu hoặc ngắt mệnh đề không
        while True:
            # Ưu tiên tìm dấu chấm câu kết thúc
            sentence_match = self.sentence_delimiters.search(self.buffer)
            if sentence_match:
                end_pos = sentence_match.end()
                ready_chunk = self.buffer[:end_pos].strip()
                self.buffer = self.buffer[end_pos:].lstrip()
                if ready_chunk:
                    chunks_to_send.append(ready_chunk)
                continue

            # Nếu độ dài đủ dài, kiểm tra dấu phẩy/chấm phẩy để ngắt sớm
            if len(self.buffer) >= self.min_clause_chars:
                clause_match = self.clause_delimiters.search(self.buffer)
                if clause_match:
                    end_pos = clause_match.end()
                    ready_chunk = self.buffer[:end_pos].strip()
                    self.buffer = self.buffer[end_pos:].lstrip()
                    if ready_chunk:
                        chunks_to_send.append(ready_chunk)
                    continue

            # Nếu buffer quá dài vượt ngưỡng an toàn
            if len(self.buffer) >= self.max_buffer_chars:
                # Cắt ở khoảng trắng gần nhất
                last_space = self.buffer.rfind(" ")
                if last_space > self.min_clause_chars:
                    ready_chunk = self.buffer[:last_space].strip()
                    self.buffer = self.buffer[last_space:].lstrip()
                    if ready_chunk:
                        chunks_to_send.append(ready_chunk)
                    continue

            break

        return chunks_to_send

    def flush(self) -> List[str]:
        """
        Xả toàn bộ phần còn lại trong buffer khi LLM kết thúc câu.
        """
        remaining = self.buffer.strip()
        self.buffer = ""
        if remaining:
            return [remaining]
        return []
