from groq import Groq
from app.core.config import settings


class GroqClient:

    def __init__(self, api_key=None):

        self.api_key = api_key or settings.GROQ_API_KEY

        self.client = Groq(
            api_key=self.api_key
        )

        self.model = settings.GROQ_MODEL

    def generate_text(
        self,
        prompt: str,
        model: str = None,
        options: dict = None
    ) -> str:

        try:

            model_name = model or self.model

            options = options or {}

            temperature = options.get(
                "temperature",
                0.3
            )

            max_tokens = options.get(
                "max_tokens",
                2048
            )

            message = (
                self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            )

            return (
                message
                .choices[0]
                .message
                .content
            )

        except Exception as e:

            print(
                f"[GROQ ERROR] {e}"
            )

            raise