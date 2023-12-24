from pydantic_settings import BaseSettings, SettingsConfigDict


# This Pydantic settings class is used to load the configuration parameters from the .env file
class Settings(BaseSettings):
    title: str = None
    description: str = None
    admin_email: str = None
    command_load: str = None
    url: str = None
    save_count_file: str = None
    hash_password: str = None
