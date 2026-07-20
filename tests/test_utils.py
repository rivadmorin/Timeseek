import pytest
from unittest.mock import patch, MagicMock
from timeseek.utils import (
    human_readable_time,
    timestamp_to_human_readable,
    get_active_app_name,
    get_active_window_title,
    is_user_active,
    get_app_category
)
from timeseek.config import USER_ACTIVITY_THRESHOLD

def test_human_readable_time():
    assert human_readable_time(45) == "45s"
    assert human_readable_time(125) == "2m 5s"
    assert human_readable_time(3665) == "1h 1m"

def test_timestamp_to_human_readable():
    # 0 timestamp is 1970-01-01 00:00:00
    assert "1970-01-01 00:00:00" in timestamp_to_human_readable(0)

def test_get_app_category():
    assert get_app_category("Code") == "Development"
    assert get_app_category("Google Chrome") == "Browsing"
    assert get_app_category("Spotify") == "Entertainment"
    assert get_app_category("UnknownApp") == "Other"
    assert get_app_category("") == "Other"

@patch("sys.platform", "win32")
@patch("timeseek.utils.win32gui")
@patch("timeseek.utils.win32process")
@patch("timeseek.utils.psutil")
def test_get_active_app_name_win32(mock_psutil, mock_win32process, mock_win32gui):
    mock_win32gui.GetForegroundWindow.return_value = 1234
    mock_win32process.GetWindowThreadProcessId.return_value = (None, 5678)

    mock_process = MagicMock()
    mock_process.name.return_value = "notepad.exe"
    mock_psutil.Process.return_value = mock_process

    assert get_active_app_name() == "notepad.exe"

@patch("sys.platform", "win32")
@patch("timeseek.utils.win32gui")
def test_get_active_window_title_win32(mock_win32gui):
    mock_win32gui.GetForegroundWindow.return_value = 1234
    mock_win32gui.GetWindowText.return_value = "Untitled - Notepad"
    assert get_active_window_title() == "Untitled - Notepad"

@patch("sys.platform", "win32")
@patch("timeseek.utils.win32api")
def test_is_user_active_win32(mock_win32api):
    # Current time 10000ms, last input 9000ms -> idle 1000ms -> 1s
    mock_win32api.GetTickCount.return_value = 10000
    mock_win32api.GetLastInputInfo.return_value = 9000
    assert is_user_active() == True # Threshold is usually much higher than 1s

    # Idle for a long time
    mock_win32api.GetTickCount.return_value = 1000000
    mock_win32api.GetLastInputInfo.return_value = 9000
    assert is_user_active() == False

@patch("sys.platform", "linux")
@patch("subprocess.Popen")
def test_get_active_app_name_linux(mock_popen):
    mock_proc_id = MagicMock()
    mock_proc_id.communicate.return_value = (b'window id # 0x12345\n', b'')
    mock_proc_id.returncode = 0

    mock_proc_class = MagicMock()
    mock_proc_class.communicate.return_value = (b'WM_CLASS(STRING) = "gnome-terminal-server", "Gnome-terminal"\n', b'')
    mock_proc_class.returncode = 0

    mock_popen.side_effect = [mock_proc_id, mock_proc_class]

    assert get_active_app_name() == "gnome-terminal-server"

@patch("sys.platform", "linux")
@patch("subprocess.check_output")
def test_is_user_active_linux(mock_check_output):
    mock_check_output.return_value = b'1000\n' # 1000ms = 1s idle
    assert is_user_active() == True
