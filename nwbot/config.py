import os
import logging
from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
guild_id = int(os.getenv("GUILD_ID", "0"))
system_channel_id = int(os.getenv("SYSTEM_CHANNEL_ID", "0"))
db_path = os.getenv("DB_PATH")
log_level_config = os.getenv("LOG_LEVEL")
log_level_mapping = {'logging.DEBUG': logging.DEBUG,
                    'logging.INFO': logging.INFO,
                    'logging.WARNING': logging.WARNING,
                    'logging.ERROR': logging.ERROR,
                }
log_level = log_level_mapping.get(log_level_config)

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