import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

    if OPENAI_API_KEY is None:
        raise RuntimeError("OPENAI_API_KEY not found")


settings = Settings()
