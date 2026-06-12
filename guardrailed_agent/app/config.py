"""
Application configuration.

Loads settings from environment variables (with sensible defaults).
Use a .env file (see .env.example) when running via Docker Compose.
"""

import os


class Settings:
    # LLM provider: "groq" or "mock"
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")

    # Model name
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # API key (loaded from environment / .env)
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")

    # App metadata
    APP_NAME: str = "Guardrailed AI Agent"
    APP_VERSION: str = "1.0.0"


settings = Settings()