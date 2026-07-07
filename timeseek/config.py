import argparse
import os
import sys

def get_appdata_folder():
    """Returns the platform-specific application data folder for Timeseek."""
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise EnvironmentError("APPDATA environment variable is not set.")
        path = os.path.join(appdata, "timeseek")
    elif sys.platform == "darwin":
        path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "timeseek")
    else:  # Linux and others
        path = os.path.join(os.path.expanduser("~"), ".local", "share", "timeseek")

    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
        except Exception:
            pass
    return path

# Base directory for application data
appdata_folder = get_appdata_folder()

# Paths for database and screenshots
db_path = os.path.join(appdata_folder, "timeseek.db")
screenshots_path = os.path.join(appdata_folder, "screenshots")
if not os.path.exists(screenshots_path):
    try:
        os.makedirs(screenshots_path, exist_ok=True)
    except Exception:
        pass

# Default configuration constants
DEFAULT_PORT = 8082
DEFAULT_SIMILARITY_THRESHOLD = 0.95
# SCREENSHOT_QUALITY = 80
IDLE_SLEEP = 5
ACTIVE_SLEEP = 3
USER_ACTIVITY_THRESHOLD = 5.0
DEFAULT_RETENTION_DAYS = 30
DEFAULT_IMAGE_QUALITY = 80

# Default blacklisted apps (privacy sensitive)
DEFAULT_BLACKLIST = ["Bitwarden", "1Password", "KeePassXC", "System Settings", "System Preferences", "Keychain Access"]
DEFAULT_KEYWORD_BLACKLIST = []

# Argument parsing for CLI customization
parser = argparse.ArgumentParser(description="Timeseek - Personal Search Engine")
parser.add_argument("--primary-monitor-only", action="store_true", help="Only take screenshots of the primary monitor")
parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to run the web server on (default: {DEFAULT_PORT})")
parser.add_argument("--blacklist", type=str, default=",".join(DEFAULT_BLACKLIST), help="Comma-separated list of app names to ignore")
parser.add_argument("--keyword-blacklist", type=str, default="", help="Comma-separated list of keywords to ignore snapshots containing them")
parser.add_argument("--retention-days", type=int, default=DEFAULT_RETENTION_DAYS, help=f"Number of days to keep data (default: {DEFAULT_RETENTION_DAYS})")
parser.add_argument("--image-quality", type=int, default=DEFAULT_IMAGE_QUALITY, help=f"Quality of saved screenshots 1-100 (default: {DEFAULT_IMAGE_QUALITY})")
parser.add_argument("--ocr-lang", type=str, default="en", help="OCR language code (default: en)")

args, unknown = parser.parse_known_args()

# Process blacklist into a list
BLACKLISTED_APPS = [app.strip() for app in args.blacklist.split(",") if app.strip()]
BLACKLISTED_KEYWORDS = [kw.strip().lower() for kw in args.keyword_blacklist.split(",") if kw.strip()]
RETENTION_DAYS = args.retention_days
SCREENSHOT_QUALITY = args.image_quality
OCR_LANG = args.ocr_lang
