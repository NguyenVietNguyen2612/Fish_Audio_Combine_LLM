import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import uvicorn
import config
from src.pipeline.voice_pipeline import VoicePipeline

app = FastAPI(title="Gemini + Fish Audio Pipeline Benchmark")

# Setup templates
templates_dir = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Initialize pipeline instance
pipeline = VoicePipeline()

class ChatVoiceRequest(BaseModel):
    prompt: str
    gemini_model: Optional[str] = "gemini-3.1-flash-lite"
    voice_id: Optional[str] = None
    fish_model: Optional[str] = "s2.1-pro-free"
    language: Optional[str] = "auto"
    emotion_tag: Optional[str] = None
    speed: Optional[float] = 1.0

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/chat-voice")
async def chat_voice(req: ChatVoiceRequest):
    if not req.prompt or not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp nội dung câu hỏi (prompt).")

    # Kiểm tra API Keys
    if not config.GEMINI_API_KEY:
        raise HTTPException(
            status_code=400,
            detail="GEMINI_API_KEY chưa được cấu hình. Vui lòng thiết lập trong file .env"
        )
    if not config.FISH_AUDIO_API_KEY:
        raise HTTPException(
            status_code=400,
            detail="FISH_AUDIO_API_KEY chưa được cấu hình. Vui lòng thiết lập trong file .env"
        )

    try:
        result = pipeline.run(
            prompt=req.prompt,
            gemini_model=req.gemini_model or config.DEFAULT_GEMINI_MODEL,
            voice_id=req.voice_id if req.voice_id and req.voice_id.strip() else None,
            fish_model=req.fish_model or config.DEFAULT_FISH_MODEL,
            language=req.language or "auto",
            emotion_tag=req.emotion_tag,
            speed=req.speed or 1.0
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/audio/{filename}")
async def get_audio(filename: str):
    audio_path = config.AUDIO_OUTPUT_DIR / filename
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="File âm thanh không tồn tại.")
    return FileResponse(audio_path, media_type="audio/mpeg")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=True)
