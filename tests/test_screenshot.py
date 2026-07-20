import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from timeseek.screenshot import (
    mean_structured_similarity_index,
    is_similar,
    take_screenshots,
    record_screenshots_thread
)
from timeseek.config import DEFAULT_SIMILARITY_THRESHOLD

def test_mean_structured_similarity_index_identical():
    img = np.ones((100, 100, 3), dtype=np.uint8) * 128
    assert mean_structured_similarity_index(img, img) == pytest.approx(1.0)

def test_mean_structured_similarity_index_different():
    img1 = np.ones((100, 100, 3), dtype=np.uint8) * 128
    img2 = np.zeros((100, 100, 3), dtype=np.uint8)
    assert mean_structured_similarity_index(img1, img2) < 1.0

def test_is_similar():
    img1 = np.ones((100, 100, 3), dtype=np.uint8) * 128
    img2 = np.ones((100, 100, 3), dtype=np.uint8) * 128
    assert is_similar(img1, img2, similarity_threshold=DEFAULT_SIMILARITY_THRESHOLD)

    img3 = np.zeros((100, 100, 3), dtype=np.uint8)
    assert not is_similar(img1, img3, similarity_threshold=0.9)


@patch("timeseek.screenshot.mss.mss")
@patch("sys.platform", "linux")
@patch.dict("os.environ", {"DISPLAY": ":0"})
def test_take_screenshots_with_display(mock_mss):
    # Setup mock
    mock_sct = MagicMock()
    mock_mss.return_value.__enter__.return_value = mock_sct
    # monitor index 0 is all monitors combined, 1 is the first monitor
    mock_sct.monitors = [{"top": 0, "left": 0, "width": 800, "height": 600},
                         {"top": 0, "left": 0, "width": 800, "height": 600}]

    mock_img = MagicMock()
    # Mocking grab to return something that can be converted to a numpy array
    mock_img.__array__ = MagicMock(return_value=np.zeros((600, 800, 4), dtype=np.uint8))
    mock_sct.grab.return_value = mock_img

    screenshots = take_screenshots()

    assert len(screenshots) == 1
    assert screenshots[0].shape == (600, 800, 3) # BGRA -> RGB


@patch("sys.platform", "linux")
@patch.dict("os.environ", {}, clear=True)
def test_take_screenshots_no_display():
    screenshots = take_screenshots()
    assert len(screenshots) == 0


@patch("timeseek.screenshot.take_screenshots")
@patch("timeseek.screenshot.is_user_active")
@patch("timeseek.screenshot.get_active_app_name")
@patch("timeseek.screenshot.state")
@patch("timeseek.screenshot.time.sleep")
def test_record_screenshots_thread_paused(mock_sleep, mock_state, mock_get_app, mock_is_active, mock_take_screenshots):
    mock_state.is_paused = True

    # Run a few iterations and then break
    mock_sleep.side_effect = [None, None, KeyboardInterrupt("Break loop")]

    with pytest.raises(KeyboardInterrupt, match="Break loop"):
        record_screenshots_thread()

    assert mock_sleep.call_count == 3
    # Should not check active state or app if paused
    mock_is_active.assert_not_called()
    mock_get_app.assert_not_called()

@patch("timeseek.screenshot.take_screenshots")
@patch("timeseek.screenshot.is_user_active")
@patch("timeseek.screenshot.get_active_app_name")
@patch("timeseek.screenshot.state")
@patch("timeseek.screenshot.time.sleep")
def test_record_screenshots_thread_inactive(mock_sleep, mock_state, mock_get_app, mock_is_active, mock_take_screenshots):
    mock_state.is_paused = False
    mock_is_active.return_value = False

    mock_sleep.side_effect = [None, None, KeyboardInterrupt("Break loop")]

    with pytest.raises(KeyboardInterrupt, match="Break loop"):
        record_screenshots_thread()

    assert mock_sleep.call_count == 3
    mock_is_active.assert_called()
    mock_get_app.assert_not_called()


@patch("timeseek.screenshot.take_screenshots")
@patch("timeseek.screenshot.is_user_active")
@patch("timeseek.screenshot.get_active_app_name")
@patch("timeseek.screenshot.state")
@patch("timeseek.screenshot.time.sleep")
@patch("timeseek.screenshot.BLACKLISTED_APPS", ["SecretApp"])
def test_record_screenshots_thread_blacklisted_app(mock_sleep, mock_state, mock_get_app, mock_is_active, mock_take_screenshots):
    mock_state.is_paused = False
    mock_is_active.return_value = True
    mock_get_app.return_value = "SecretApp"

    mock_sleep.side_effect = [None, None, KeyboardInterrupt("Break loop")]

    with pytest.raises(KeyboardInterrupt, match="Break loop"):
        record_screenshots_thread()

    # take_screenshots called once for initialization
    assert mock_take_screenshots.call_count == 1
