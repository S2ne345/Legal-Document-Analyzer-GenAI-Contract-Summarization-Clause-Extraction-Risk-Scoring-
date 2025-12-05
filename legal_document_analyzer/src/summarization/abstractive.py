
from ..utils.logging_utils import get_logger
from .extractive import summarize as extractive_summarize

logger = get_logger('abstractive')


def summarize(text: str, max_chars: int = 1200) -> str:
    """Attempt abstractive summarization via transformers; fallback to extractive."""
    try:
        from transformers import pipeline
        n = min(max(200, len(text)//4), max_chars)
        summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
        out = summarizer(text, max_length=min(512, n//5), min_length=80, do_sample=False)
        return out[0]['summary_text']
    except Exception as e:
        logger.warning(f"Transformers unavailable or failed ({e}); using extractive summarization.")
        return extractive_summarize(text)
