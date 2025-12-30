from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "gst_recon.db"

SANDBOX_BASE_URL = "https://test-api.sandbox.co.in"

API_VERSION = "1.0.0"
