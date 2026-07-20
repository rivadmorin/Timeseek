import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from timeseek.ocr import extract_text_from_image, get_predictor
import timeseek.ocr as ocr_module

def test_extract_text_from_image_success():
    # Mock the predictor object
    mock_predictor = MagicMock()

    # Mock the result export structure
    mock_result = MagicMock()
    mock_result.export.return_value = {
        "pages": [
            {
                "blocks": [
                    {
                        "lines": [
                            {"words": [{"value": "Hello"}, {"value": "World"}]},
                            {"words": [{"value": "Test"}]}
                        ]
                    }
                ]
            }
        ]
    }
    mock_predictor.return_value = mock_result

    with patch("timeseek.ocr.get_predictor", return_value=mock_predictor):
        image_array = np.zeros((100, 100, 3), dtype=np.uint8)
        text = extract_text_from_image(image_array)
        assert text == "Hello World\nTest"

def test_extract_text_from_image_exception():
    with patch("timeseek.ocr.get_predictor", side_effect=Exception("Test Error")):
        image_array = np.zeros((100, 100, 3), dtype=np.uint8)
        text = extract_text_from_image(image_array)
        assert text == ""

def test_get_predictor_success():
    # Reset global _predictor
    ocr_module._predictor = None
    with patch("timeseek.ocr.ocr_predictor") as mock_ocr_predictor:
        mock_ocr_predictor.return_value = "mocked_predictor"
        predictor1 = get_predictor()
        predictor2 = get_predictor()
        assert predictor1 == "mocked_predictor"
        assert predictor1 is predictor2
        mock_ocr_predictor.assert_called_once()

def test_get_predictor_exception():
    ocr_module._predictor = None
    with patch("timeseek.ocr.ocr_predictor", side_effect=Exception("Init Error")):
        with pytest.raises(Exception, match="Init Error"):
            get_predictor()
