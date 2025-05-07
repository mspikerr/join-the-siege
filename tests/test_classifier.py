import pytest
from src.classifier import classify_text, ml_classify_text

@pytest.mark.parametrize("text,expected", [
    ("This is an invoice with amount due", "invoice"),
    ("Driver's License #XYZ123", "drivers_license"),
    ("Statement for bank account", "bank_statement"),
    ("Random content with no keywords", "unknown file")
])
def test_classify_text(text, expected):
    assert classify_text(text) == expected

def test_ml_classify_text_predicts():
    # Only test that ML prediction returns a string, assuming model is loaded
    result = ml_classify_text("Some example input without keywords")
    assert isinstance(result, str)