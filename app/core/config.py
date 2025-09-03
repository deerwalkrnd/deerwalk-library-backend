from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Deerwalk Library API"
    admin_email: str = "library@sifal.deerwalk.edu.np"
    admin_password: str = "librarian!123#"
    default_pagination: int = 10
    default_fine_amount: int = 3
    jtw_key: str = "hahahahahahayolobotsharu"
    database_url: str

    s3_access_key_id: str
    s3_secret_access_key: str
    s3_bucket_name: str
    s3_region_name: str

    smtp_username: str
    smtp_password: str
    smtp_use_tls: bool = True
    smtp_host: str
    smtp_port: int

    google_client_id: str
    google_client_secret: str
    google_redirect_url: str

    redis_url: str
    frontend_url: str

    model_config = SettingsConfigDict(env_file=".env.dev.aws")
