from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    title: str = "FastAPIBuilder"
    description: str = "default"
    app_name: str = "Awesome"
    admin_email: str = "Et"
    items_per_user: int = 50
    #model_config = SettingsConfigDict(env_file=".env")
