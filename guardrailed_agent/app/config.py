import os


class Settings:
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
    APP_NAME: str = "Guardrailed AI Agent"
    APP_VERSION: str = "1.0.0"


settings = Settings()
