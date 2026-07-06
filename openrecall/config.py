import argparse
import os

# Base directory for application data
appdata_folder = os.path.join(os.path.expanduser("~"), ".openrecall")
if not os.path.exists(appdata_folder):
    os.makedirs(appdata_folder)

# Paths for database and screenshots
db_path = os.path.join(appdata_folder, "openrecall.db")
screenshots_path = os.path.join(appdata_folder, "screenshots")
if not os.path.exists(screenshots_path):
    os.makedirs(screenshots_path)

# Default configuration constants
DEFAULT_PORT = 8082
DEFAULT_SIMILARITY_THRESHOLD = 0.9

# Argument parsing for CLI customization
parser = argparse.ArgumentParser(description="OpenRecall - Personal Search Engine")
parser.add_argument("--primary-monitor-only", action="store_true", help="Only take screenshots of the primary monitor")
parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to run the web server on (default: {DEFAULT_PORT})")
args, unknown = parser.parse_known_args()
