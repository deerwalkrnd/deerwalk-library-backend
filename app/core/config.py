from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Deerwalk Library API"
    admin_email: str = "library@sifal.deerwalk.edu.np"
    admin_password: str = "librarian!123#"
    default_pagination: int = 10
    default_fine_amount: int = 3
    database_url: str

    model_config = SettingsConfigDict(env_file=".env.dev")
