import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Ensure system certificates are used (supports local/corporate proxy certs)
if not os.getenv("SSL_CERT_FILE") and os.path.exists("/etc/ssl/certs/ca-certificates.crt"):
    os.environ["SSL_CERT_FILE"] = "/etc/ssl/certs/ca-certificates.crt"

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
FISH_AUDIO_API_KEY = os.getenv("FISH_AUDIO_API_KEY", "")

# Default Models & Settings
DEFAULT_GEMINI_MODEL = os.getenv("DEFAULT_GEMINI_MODEL", "gemini-3.1-flash-lite")
DEFAULT_FISH_MODEL = os.getenv("DEFAULT_FISH_MODEL", "s2.1-pro-free")
DEFAULT_FISH_VOICE_ID = os.getenv("DEFAULT_FISH_VOICE_ID", "d6126bec5abc465fb965335e043aafbb")
DEFAULT_FISH_LATENCY = os.getenv("DEFAULT_FISH_LATENCY", "balanced")  # "normal" or "balanced"

# Voice Presets
VOICE_PRESETS = {
    "vi_male": {"name": "Phi Hùng (Nam Tiếng Việt)", "id": "d6126bec5abc465fb965335e043aafbb"},
    "vi_female": {"name": "Nữ VN (Truyền cảm)", "id": "4348ff4c4ce043d58866790fdc670400"},
    "en_sarah": {"name": "Sarah (Nữ Tiếng Anh)", "id": "933563129e564b19a115bedd57b7406a"},
    "en_male": {"name": "Energetic Male (Nam EN)", "id": "802e3bc2b27e49c2995d23ef70e6ac89"}
}

# Output directories
OUTPUT_DIR = BASE_DIR / "outputs"
AUDIO_OUTPUT_DIR = OUTPUT_DIR / "audio_samples"
BENCHMARK_OUTPUT_DIR = OUTPUT_DIR / "benchmarks"

AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BENCHMARK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
