import os
import sys
import argparse

def parse_args():
    # Only parse args if running as main or if explicitly called
    # Avoiding parse_args() during library import (e.g. by pytest)
    parser = argparse.ArgumentParser(description="OpenRecall")

    parser.add_argument(
        "--storage-path",
        default=None,
        help="Path to store the screenshots and database",
    )

    parser.add_argument(
        "--primary-monitor-only",
        action="store_true",
        help="Only record the primary monitor",
        default=False,
    )

    # If we are in pytest, ignore unknown args or don't parse
    if "pytest" in sys.modules or "pytest" in sys.argv[0]:
        args, _ = parser.parse_known_args()
    else:
        args = parser.parse_args()
    return args

args = parse_args()


def get_appdata_folder(app_name="openrecall"):
    if sys.platform == "win32":
        appdata = os.getenv("APPDATA")
        if not appdata:
            raise EnvironmentError("APPDATA environment variable is not set.")
        path = os.path.join(appdata, app_name)
    elif sys.platform == "darwin":
        home = os.path.expanduser("~")
        path = os.path.join(home, "Library", "Application Support", app_name)
    else:
        home = os.path.expanduser("~")
        path = os.path.join(home, ".local", "share", app_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


if args.storage_path:
    appdata_folder = args.storage_path
    screenshots_path = os.path.join(appdata_folder, "screenshots")
    db_path = os.path.join(appdata_folder, "recall.db")
else:
    appdata_folder = get_appdata_folder()
    db_path = os.path.join(appdata_folder, "recall.db")
    screenshots_path = os.path.join(appdata_folder, "screenshots")

if not os.path.exists(screenshots_path):
    try:
        os.makedirs(screenshots_path)
    except:
        pass
