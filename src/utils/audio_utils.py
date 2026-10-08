from pathlib import Path
from typing import Optional
from mutagen.mp3 import MP3

def get_audio_duration_seconds(file_path: Path) -> float:
    """
    Tính độ dài file audio MP3 theo giây bằng mutagen (không phụ thuộc ffmpeg).
    """
    try:
        audio = MP3(str(file_path))
        return round(audio.info.length, 2)
    except Exception:
        # Fallback ước tính nếu file header bị thiếu: 128kbps = 16000 bytes/sec
        size_bytes = file_path.stat().st_size
        return round(size_bytes / 16000, 2)
