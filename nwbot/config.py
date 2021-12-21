import os
import logging
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
SYSTEM_CHANNEL_ID = int(os.getenv("SYSTEM_CHANNEL_ID", "0"))
ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME", "admin")
DB_PATH = os.getenv("DB_PATH", "db.pickle")
log_level_config = os.getenv("LOG_LEVEL", "INFO")
log_level_mapping = {'DEBUG': logging.DEBUG,
                    'INFO': logging.INFO,
                    'WARNING': logging.WARNING,
                    'ERROR': logging.ERROR,
                }
LOG_LEVEL = log_level_mapping.get(log_level_config)

PROFESSIONS = {
    "Waffenschmiedekunst": "WFK",
    "Rüstungsschmiedekunst": "RSK",
    "Ingenieurskunst": "ING",
    "Juwelenschleiferei": "JUW",
    "Arkana": "ARK",
    "Kochkunst": "KOK",
    "Tischlerei": "TSL",
    "Schmelzen": "SMZ",
    "Holzverarbeitung": "HLZ",
    "Lederverarbeitung": "LDR",
    "Weberei": "WBR",
    "Steinmetzkunst": "SMK"
}