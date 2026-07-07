from doctr.models import ocr_predictor

# Initialize the OCR model (loads on first use)
_predictor = None


def get_predictor():
    """Initializes and returns the OCR predictor."""
    global _predictor
    if _predictor is None:
        _predictor = ocr_predictor(
            det_arch="db_resnet50", reco_arch="crnn_vgg16_bn", pretrained=True
        )
    return _predictor


def extract_text_from_image(image_array) -> str:
    """Extracts text from a numpy image array using doctr OCR."""
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
        print(f"Error during OCR extraction: {e}")
        return ""
