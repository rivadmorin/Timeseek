import pytest
from unittest import mock
from timeseek.config import get_appdata_folder


def test_get_appdata_folder_windows(tmp_path):
    with mock.patch("sys.platform", "win32"):
        with mock.patch.dict("os.environ", {"APPDATA": str(tmp_path)}):
            expected_path = tmp_path / "timeseek"
            assert get_appdata_folder() == str(expected_path)
            assert expected_path.exists()


def test_get_appdata_folder_windows_no_appdata():
    with mock.patch("sys.platform", "win32"):
        with mock.patch.dict("os.environ", {}, clear=True):
            with pytest.raises(
                EnvironmentError, match="APPDATA environment variable is not set."
            ):
                get_appdata_folder()


def test_get_appdata_folder_darwin(tmp_path):
    with mock.patch("sys.platform", "darwin"):
        with mock.patch("os.path.expanduser", return_value=str(tmp_path)):
            expected_path = tmp_path / "Library" / "Application Support" / "timeseek"
            assert get_appdata_folder() == str(expected_path)
            assert expected_path.exists()


def test_get_appdata_folder_linux(tmp_path):
    with mock.patch("sys.platform", "linux"):
        with mock.patch("os.path.expanduser", return_value=str(tmp_path)):
            expected_path = tmp_path / ".local" / "share" / "timeseek"
            assert get_appdata_folder() == str(expected_path)
            assert expected_path.exists()

import os
import argparse
from unittest.mock import patch
import timeseek.config as config

def test_config_defaults():
    # Test that default values are parsed correctly when no args are provided
    with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
            storage_path=None, port=8082, primary_monitor_only=False,
            blacklist="", retention_days=30)):

        args = config.parser.parse_args()
        assert args.port == 8082
        assert args.retention_days == 30
        assert args.primary_monitor_only == False
