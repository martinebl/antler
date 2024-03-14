import pytest
from llmtest.detectors import Detector
from llmtest.detectors.simpledetector import SimpleDetector
from llmtest.detectors.regexdetector import RegexDetector

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