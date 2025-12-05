
from src.summarization.extractive import summarize

sample = "This Agreement is between A and B. The payment terms are Net 30. Termination for convenience is permitted. Confidential information must be protected."

def test_summary_runs():
    out = summarize(sample, max_sentences=2)
    assert isinstance(out, str)
    assert len(out) > 0
