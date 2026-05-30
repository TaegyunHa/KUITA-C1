"""Guards the hard rule (CLAUDE.md / README): "What now?" stays English, never translated."""

from app.llm import personalise
from app.routes import feed


def test_feed_label_is_the_english_brand():
    assert feed.LABEL == "What now?"


def test_personalise_prompt_forbids_translating_the_brand():
    system = personalise.SYSTEM
    assert '"What now?"' in system
    assert "translate" in system.lower()
    assert "never appear" in system.lower()
