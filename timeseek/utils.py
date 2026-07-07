import sys
import datetime
import re
import subprocess
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
    """Converts seconds into a human-readable string (e.g., '1h 2m 3s')."""
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
    """Converts a Unix timestamp to a human-readable date and time string."""
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def get_active_app_name_windows() -> str:
    """Gets the name of the active application on Windows."""
    if win32gui is None or win32process is None or psutil is None:
        return ""
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        return process.name()
    except Exception:
        return ""

def get_active_window_title_windows() -> str:
    """Gets the title of the active window on Windows."""
    if win32gui is None:
        return ""
    try:
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)
    except Exception:
        return ""

def get_active_app_name_osx() -> str:
    """Gets the name of the active application on macOS."""
    if NSWorkspace is None:
        return ""
    try:
        workspace = NSWorkspace.sharedWorkspace()
        active_app = workspace.frontmostApplication()
        return active_app.localizedName()
    except Exception:
        return ""

def get_active_window_title_osx() -> str:
    """Gets the title of the active window on macOS."""
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

def get_active_app_name_linux() -> str:
    """Gets the name of the active application on Linux."""
    if subprocess is None:
        return ""
    try:
        # Get active window ID
        active_window_cmd = ['xprop', '-root', '_NET_ACTIVE_WINDOW']
        active_window_proc = subprocess.Popen(active_window_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = active_window_proc.communicate(timeout=1)
        if active_window_proc.returncode != 0:
            return ""

        match = re.search(rb'window id # (0x[0-9a-fA-F]+)', stdout)
        if not match:
            return ""
        window_id = match.group(1).decode('utf-8')

        # Get WM_CLASS
        class_cmd = ['xprop', '-id', window_id, 'WM_CLASS']
        class_proc = subprocess.Popen(class_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = class_proc.communicate(timeout=1)
        if class_proc.returncode != 0:
            return ""

        match = re.search(rb'WM_CLASS\(STRING\) = "([^"]+)"(?:, "([^"]+)")?', stdout)
        if match:
            return match.group(1).decode('utf-8')
        return ""
    except Exception:
         return ""

def get_active_window_title_linux() -> str:
    """Gets the title of the active window on Linux."""
    if subprocess is None:
        return ""
    try:
        active_window_cmd = ['xprop', '-root', '_NET_ACTIVE_WINDOW']
        active_window_proc = subprocess.Popen(active_window_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = active_window_proc.communicate(timeout=1)
        if active_window_proc.returncode != 0:
            return ""

        match = re.search(rb'window id # (0x[0-9a-fA-F]+)', stdout)
        if not match:
            return ""
        window_id = match.group(1).decode('utf-8')

        for prop_name in ['_NET_WM_NAME', 'WM_NAME']:
            title_cmd = ['xprop', '-id', window_id, prop_name]
            title_proc = subprocess.Popen(title_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = title_proc.communicate(timeout=1)

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

def get_active_app_name() -> str:
    """Gets the active application name for the current platform."""
    if sys.platform == "win32":
        return get_active_app_name_windows()
    elif sys.platform == "darwin":
        return get_active_app_name_osx()
    elif sys.platform.startswith("linux"):
        return get_active_app_name_linux()
    else:
        return ""

def get_active_window_title() -> str:
    """Gets the active window title for the current platform."""
    if sys.platform == "win32":
        return get_active_window_title_windows()
    elif sys.platform == "darwin":
        return get_active_window_title_osx()
    elif sys.platform.startswith("linux"):
        return get_active_window_title_linux()
    else:
        return ""

def is_user_active_osx() -> bool:
    """Checks if the user is active on macOS based on HID idle time."""
    if subprocess is None:
        return True
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

def is_user_active_windows() -> bool:
    """Checks if the user is active on Windows based on last input time."""
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

def is_user_active_linux() -> bool:
    """Checks if the user is active on Linux using xprintidle."""
    if subprocess is None:
        return True
    try:
        output = subprocess.check_output(['xprintidle'], timeout=1).decode()
        idle_milliseconds = int(output.strip())
        idle_seconds = idle_milliseconds / 1000.0
        return idle_seconds < USER_ACTIVITY_THRESHOLD
    except Exception:
        return True

def is_user_active() -> bool:
    """Checks if the user is active on the current platform."""
    if sys.platform == "win32":
        return is_user_active_windows()
    elif sys.platform == "darwin":
        return is_user_active_osx()
    elif sys.platform.startswith("linux"):
        return is_user_active_linux()
    else:
        return True
