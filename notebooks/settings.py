from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Setup to define a user from the environment variables.

    Need to have a .env file with the following variables:

    Env Vars:
        OPENAI_API_TOKEN (str): The API token for the OpenAI API.

    """
    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_token: str
