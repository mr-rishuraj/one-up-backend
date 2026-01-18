import os
from dotenv import load_dotenv

load_dotenv()  # works locally, ignored in Railway (fine)


class Settings:
    def __init__(self):
        self.OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

        if not self.OPENAI_API_KEY:
            print("⚠️ WARNING: OPENAI_API_KEY not set. AI analysis will not work.")


settings = Settings()
