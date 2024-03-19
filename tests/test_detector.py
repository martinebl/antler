import pytest
from llmtest.detectors import Detector, SimpleDetector, RegexDetector, NotDetector, AndDetector

@pytest.fixture
def targets():
    return ["Test", "test", "Target", "target"]

def test_base_detector_not_implemented():
    with pytest.raises(NotImplementedError):
        Detector().detect("prompt")

def test_detect_targets(targets):
    detector = SimpleDetector(targets)
    assert detector.detect(''.join(targets))

@pytest.mark.parametrize("answer, patterns, detection", [
    ("This is a prompt", [r"prompt"], True),
    ("Thisisapromptwithoutspaces", [r"\s"], False),
    ("  def thisIsAFunction:", [r"def \w+:"], True),
])
def test_detect_regex(answer: str, patterns: list[str], detection: bool):
    detector = RegexDetector(patterns)
    assert detector.detect(answer) == detection


@pytest.mark.parametrize("answer, patterns, detection", [
    ("This is an answer", ["answer"], False),
    ("This is an answer", ["bla", "skipdidi", "boop"], True)
])
def test_not_detector(answer: str, patterns: list[str], detection: bool):
    detector = NotDetector(SimpleDetector(patterns))
    assert detector.detect(answer) == detection

@pytest.mark.parametrize("answer, detectors, detection", [
    ("This is just an answer", [SimpleDetector(["just"]), NotDetector(SimpleDetector(["not", "to", "be", "found"]))], True),
    ("This is just an answer", [SimpleDetector(["just"]), NotDetector(SimpleDetector(["This"]))], False),
    ("This is just an answer", [SimpleDetector(["skippidi"]), NotDetector(SimpleDetector(["something", "not", "there"]))], False),
])
def test_and_detector(answer: str, detectors: list[Detector], detection: bool):
    detector = AndDetector(detectors)
    assert detector.detect(answer) == detection