
from pathlib import Path
from typing import Dict, Any
from .ocr import ocr_image_to_text
from ..utils.logging_utils import get_logger

logger = get_logger('document_loader')


def load_text(path: str | Path) -> Dict[str, Any]:
    """Load text from PDF, DOCX, or TXT. Uses OCR for images if possible."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    ext = p.suffix.lower()
    if ext == '.pdf':
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(p)
            texts = []
            for page in doc:
                texts.append(page.get_text())
            return {'text': '
'.join(texts), 'meta': {'pages': doc.page_count, 'type': 'pdf'}}
        except Exception as e:
            logger.warning(f"PDF parsing fallback to OCR due to: {e}")
            # Attempt rudimentary OCR by rasterizing pages
            try:
                import fitz
                import pytesseract
                from PIL import Image
                doc = fitz.open(p)
                texts = []
                for page in doc:
                    pix = page.get_pixmap()
                    img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
                    texts.append(pytesseract.image_to_string(img))
                return {'text': '
'.join(texts), 'meta': {'pages': doc.page_count, 'type': 'pdf_ocr'}}
            except Exception as e2:
                raise RuntimeError(f"Failed to parse PDF: {e2}")
    elif ext == '.docx':
        try:
            import docx
            doc = docx.Document(p)
            text = '
'.join([para.text for para in doc.paragraphs])
            return {'text': text, 'meta': {'type': 'docx'}}
        except Exception as e:
            raise RuntimeError(f"Failed to parse DOCX: {e}")
    elif ext in ('.txt', '.md'):
        return {'text': p.read_text(encoding='utf-8'), 'meta': {'type': 'text'}}
    elif ext in ('.png', '.jpg', '.jpeg', '.tiff'):
        return {'text': ocr_image_to_text(p), 'meta': {'type': 'image_ocr'}}
    else:
        raise ValueError(f"Unsupported file type: {ext}")
