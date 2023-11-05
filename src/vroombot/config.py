from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv


@dataclass
class GoogleSheetsConfig:
    sheet_id: str
    json_file: Path


@dataclass
class Config:
    google_sheets: GoogleSheetsConfig
    telegram_bot_key: str
    secrets_dir: Path


def load_config() -> Config:
    secrets_file_path = Path(__file__).parent / ".secrets"
    if not secrets_file_path.exists():
        raise FileNotFoundError(f"Could not find {str(secrets_file_path)}")
    load_result = load_dotenv(secrets_file_path)
    if not load_result:
        raise FileNotFoundError(f"Could not read {str(secrets_file_path)}")

    return Config(
        google_sheets=GoogleSheetsConfig(
            sheet_id=os.getenv("GOOGLE_SHEETS_SHEET_ID"),
            json_file=secrets_file_path.parent / "google-sheets-bot-auth.json",
        ),
        telegram_bot_key=os.getenv("TELEGRAM_BOT_KEY"),
        secrets_dir=secrets_file_path.parent,
    )
