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
DEFAULT_SIMILARITY_THRESHOLD = 0.9

# Argument parsing for CLI customization
parser = argparse.ArgumentParser(description="Timeseek - Personal Search Engine")
parser.add_argument("--primary-monitor-only", action="store_true", help="Only take screenshots of the primary monitor")
parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to run the web server on (default: {DEFAULT_PORT})")
args, unknown = parser.parse_known_args()
