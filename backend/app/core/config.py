from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Agentic SQL Insights"
    ENV: str = "development"
    
    # GROQ LLM Configuration
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # Database Configuration
    DATABASE_TIMEOUT: int = 30
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "agentic_ai"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
