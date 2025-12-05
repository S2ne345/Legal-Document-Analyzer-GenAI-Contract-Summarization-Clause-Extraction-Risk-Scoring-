
from pathlib import Path
from ..utils.logging_utils import get_logger

logger = get_logger('ocr')


def ocr_image_to_text(path: str | Path) -> str:
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(path)
        return pytesseract.image_to_string(img)
    except Exception as e:
        logger.error(f"OCR failed. Ensure Tesseract is installed. Error: {e}")
        return ''
