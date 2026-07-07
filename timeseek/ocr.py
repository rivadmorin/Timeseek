from typing import Optional
import numpy as np
from doctr.models import ocr_predictor
import logging

logger = logging.getLogger(__name__)

# Initialize the OCR model (loads on first use)
_predictor = None


def get_predictor():
    """Initializes and returns the OCR predictor.

    Returns:
        The docTR OCR predictor instance.
    """
    global _predictor
    if _predictor is None:
        try:
            _predictor = ocr_predictor(
                det_arch="db_resnet50", reco_arch="crnn_vgg16_bn", pretrained=True
            )
            logger.info("docTR OCR predictor initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize docTR OCR predictor: {e}")
            raise
    return _predictor


def extract_text_from_image(image_array: np.ndarray) -> str:
    """Extracts text from a numpy image array using docTR OCR.

    Args:
        image_array: Numpy array representing the image (RGB).

    Returns:
        Extracted text as a string with lines separated by newlines.
    """
    try:
        predictor = get_predictor()
        result = predictor([image_array])
        export = result.export()

        text_lines = []
        for page in export["pages"]:
            for block in page["blocks"]:
                for line in block["lines"]:
                    line_text = " ".join([word["value"] for word in line["words"]])
                    text_lines.append(line_text)

        return "\n".join(text_lines)
    except Exception as e:
        logger.error(f"Error during OCR extraction: {e}")
        return ""
