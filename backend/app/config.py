from pathlib import Path
import os
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = REPO_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / "data" / "processed"
CACHE_DIR = BASE_DIR.parent / "data" / "cache"

APP_NAME = "Montgomery Civic Copilot API"
APP_VERSION = "0.1.0"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

BRIGHTDATA_API_KEY = os.getenv("BRIGHTDATA_API_KEY", "")
BRIGHTDATA_ZONE_WEB_UNLOCKER = os.getenv("BRIGHTDATA_ZONE_WEB_UNLOCKER", "web_unlocker")
BRIGHTDATA_ZONE_SERP = os.getenv("BRIGHTDATA_ZONE_SERP", "")

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

SERVICES_FILE = DATA_DIR / "services.json"
DISTRICTS_FILE = DATA_DIR / "districts.json"
TRANSPORT_FILE = DATA_DIR / "transport.json"
DEMO_EXAMPLES_FILE = DATA_DIR / "demo_examples.json"
DEMO_ADDRESSES_FILE = DATA_DIR / "demo_addresses.json"
