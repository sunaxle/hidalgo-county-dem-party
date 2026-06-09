from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    google_drive_path: Optional[str] = "/Users/dr3/Library/CloudStorage/GoogleDrive-romerodeab@gmail.com/My Drive"
    dropzone_relative_path: str = "Work/Agent Dropzone"
    audio_extensions: List[str] = [".m4a", ".mp3", ".wav", ".aac", ".ogg", ".flac"]
    server_port: int = 8001
    log_server_port: int = 8003

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()
