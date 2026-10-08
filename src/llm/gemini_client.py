import time
from typing import Generator, Dict, Any, Optional
from google import genai
from google.genai import types
import config

class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.GEMINI_API_KEY
        self._client = None
        if self.api_key:
            self._client = genai.Client(api_key=self.api_key)

    @property
    def client(self):
        if not self.api_key:
            self.api_key = config.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY chưa được thiết lập trong .env.")
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def generate_stream(
        self,
        prompt: str,
        model: str = "gemini-2.5-flash",
        system_instruction: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Stream response từ Gemini LLM và tính toán TTFT.
        Yields:
            Dict: {
                "token": str,
                "is_first": bool,
                "elapsed_ms": float,
                "ttft_ms": Optional[float]
            }
        """
        start_time = time.perf_counter()
        first_token_received = False
        ttft_ms = None

        config_params = types.GenerateContentConfig(
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            system_instruction=system_instruction if system_instruction else None
        )

        response_stream = self.client.models.generate_content_stream(
            model=model,
            contents=prompt,
            config=config_params
        )

        for chunk in response_stream:
            token_text = chunk.text or ""
            if not token_text:
                continue

            current_time = time.perf_counter()
            elapsed_ms = (current_time - start_time) * 1000

            is_first = False
            if not first_token_received:
                first_token_received = True
                is_first = True
                ttft_ms = elapsed_ms

            yield {
                "token": token_text,
                "is_first": is_first,
                "elapsed_ms": elapsed_ms,
                "ttft_ms": ttft_ms,
                "start_time": start_time
            }
