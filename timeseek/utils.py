import sys
import datetime
import re
import subprocess
from typing import Dict, List, Optional
from timeseek.config import USER_ACTIVITY_THRESHOLD

# Platform-specific imports with error handling
try:
    import psutil
    import win32gui
    import win32process
    import win32api
except ImportError:
    psutil = None
    win32gui = None
    win32process = None
    win32api = None

try:
    from AppKit import NSWorkspace
except ImportError:
    NSWorkspace = None

try:
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGNullWindowID,
        kCGWindowListOptionOnScreenOnly,
    )
except ImportError:
    CGWindowListCopyWindowInfo = None
    kCGNullWindowID = None
    kCGWindowListOptionOnScreenOnly = None

def human_readable_time(seconds: int) -> str:
    """Converts seconds into a human-readable string.

    Args:
        seconds: Number of seconds.

    Returns:
        String formatted as '1h 2m 3s' or similar.
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{hours}h {remaining_minutes}m"

def timestamp_to_human_readable(timestamp: int) -> str:
    """Converts a Unix timestamp to a human-readable date and time string.

    Args:
        timestamp: Unix timestamp.

    Returns:
        Formatted datetime string.
    """
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def get_active_app_name() -> str:
    """Gets the active application name for the current platform.

    Returns:
        The name of the frontmost application.
    """
    if sys.platform == "win32":
        if win32gui is None or win32process is None or psutil is None:
            return ""
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name()
        except Exception:
            return ""
    elif sys.platform == "darwin":
        if NSWorkspace is None:
            return ""
        try:
            workspace = NSWorkspace.sharedWorkspace()
            active_app = workspace.frontmostApplication()
            return active_app.localizedName()
        except Exception:
            return ""
    elif sys.platform.startswith("linux"):
        try:
            # Get active window ID
            active_window_cmd = ['xprop', '-root', '_NET_ACTIVE_WINDOW']
            active_window_proc = subprocess.Popen(active_window_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = active_window_proc.communicate(timeout=1)
            if active_window_proc.returncode != 0:
                return ""

            match = re.search(rb'window id # (0x[0-9a-fA-F]+)', stdout)
            if not match:
                return ""
            window_id = match.group(1).decode('utf-8')

            # Get WM_CLASS
            class_cmd = ['xprop', '-id', window_id, 'WM_CLASS']
            class_proc = subprocess.Popen(class_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = class_proc.communicate(timeout=1)
            if class_proc.returncode != 0:
                return ""

            match = re.search(rb'WM_CLASS\(STRING\) = "([^"]+)"(?:, "([^"]+)")?', stdout)
            if match:
                return match.group(1).decode('utf-8')
            return ""
        except Exception:
             return ""
    else:
        return ""

def get_active_window_title() -> str:
    """Gets the active window title for the current platform.

    Returns:
        The title of the frontmost window.
    """
    if sys.platform == "win32":
        if win32gui is None:
            return ""
        try:
            hwnd = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(hwnd)
        except Exception:
            return ""
    elif sys.platform == "darwin":
        if CGWindowListCopyWindowInfo is None:
            return ""
        try:
            window_list = CGWindowListCopyWindowInfo(
                kCGWindowListOptionOnScreenOnly, kCGNullWindowID
            )
            for window in window_list:
                if window.get("kCGWindowIsOnscreen") and window.get("kCGWindowLayer") == 0:
                    return window.get("kCGWindowTitle", "")
            return ""
        except Exception:
            return ""
    elif sys.platform.startswith("linux"):
        try:
            active_window_cmd = ['xprop', '-root', '_NET_ACTIVE_WINDOW']
            active_window_proc = subprocess.Popen(active_window_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = active_window_proc.communicate(timeout=1)
            if active_window_proc.returncode != 0:
                return ""

            match = re.search(rb'window id # (0x[0-9a-fA-F]+)', stdout)
            if not match:
                return ""
            window_id = match.group(1).decode('utf-8')

            for prop_name in ['_NET_WM_NAME', 'WM_NAME']:
                title_cmd = ['xprop', '-id', window_id, prop_name]
                title_proc = subprocess.Popen(title_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, _ = title_proc.communicate(timeout=1)

                if title_proc.returncode == 0:
                    if prop_name == '_NET_WM_NAME':
                        match = re.search(rb'_NET_WM_NAME\(UTF8_STRING\) = "([^"]*)"', stdout)
                    else:
                        match = re.search(rb'WM_NAME\([^)]*\) = "([^"]*)"', stdout)

                    if match:
                        return match.group(1).decode('utf-8', errors='replace')
            return ""
        except Exception:
            return ""
    else:
        return ""

def is_user_active() -> bool:
    """Checks if the user is active on the current platform based on input/idle time.

    Returns:
        True if the user has provided input recently, False otherwise.
    """
    if sys.platform == "win32":
        if win32api is None:
            return True
        try:
            last_input_info = win32api.GetLastInputInfo()
            current_time = win32api.GetTickCount()
            idle_milliseconds = current_time - last_input_info
            idle_seconds = idle_milliseconds / 1000.0
            return idle_seconds < USER_ACTIVITY_THRESHOLD
        except Exception:
            return True
    elif sys.platform == "darwin":
        try:
            output = subprocess.check_output(
                ["ioreg", "-c", "IOHIDSystem", "-r", "-k", "HIDIdleTime"], timeout=1
            ).decode()
            for line in output.splitlines():
                if "HIDIdleTime" in line:
                    idle_time = int(line.split("=")[-1].strip())
                    idle_seconds = idle_time / 1_000_000_000
                    return idle_seconds < USER_ACTIVITY_THRESHOLD
            return True
        except Exception:
            return True
    elif sys.platform.startswith("linux"):
        try:
            output = subprocess.check_output(['xprintidle'], timeout=1).decode()
            idle_milliseconds = int(output.strip())
            idle_seconds = idle_milliseconds / 1000.0
            return idle_seconds < USER_ACTIVITY_THRESHOLD
        except Exception:
            return True
    else:
        return True

def get_app_category(app_name: str) -> str:
    """Categorizes an application based on its name.

    Args:
        app_name: Name of the application.

    Returns:
        Category string (e.g., 'Development', 'Productivity').
    """
    if not app_name:
        return "Other"

    app_name = app_name.lower()
    categories = {
        "Development": ["code", "visual studio", "terminal", "iterm", "pycharm", "intellij", "docker", "github", "sublime", "vim"],
        "Productivity": ["word", "excel", "powerpoint", "sheets", "docs", "slides", "notion", "obsidian", "slack", "teams", "discord", "outlook", "mail", "notes"],
        "Browsing": ["chrome", "firefox", "safari", "edge", "brave", "opera"],
        "Social": ["whatsapp", "telegram", "messenger", "twitter", "facebook", "instagram", "linkedin"],
        "Entertainment": ["spotify", "netflix", "youtube", "vlc", "mpv", "steam", "games"],
        "System": ["settings", "preferences", "finder", "explorer", "task manager", "activity monitor"]
    }
    for category, keywords in categories.items():
        if any(kw in app_name for kw in keywords):
            return category
    return "Other"
