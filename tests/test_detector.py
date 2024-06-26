import pytest
from antler.detectors import *

@pytest.fixture
def targets():
    return ["Test", "test", "Target", "target"]

def test_base_detector_not_implemented():
    with pytest.raises(NotImplementedError):
        Detector().detect("prompt")

def test_detect_targets(targets):
    detector = KeyWordDetector(targets)
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
    detector = NotDetector(KeyWordDetector(patterns))
    assert detector.detect(answer) == detection

@pytest.mark.parametrize("answer, detectors, detection", [
    ("This is just an answer", [KeyWordDetector(["just"]), NotDetector(KeyWordDetector(["not", "to", "be", "found"]))], True),
    ("This is just an answer", [KeyWordDetector(["just"]), NotDetector(KeyWordDetector(["This"]))], False),
    ("This is just an answer", [KeyWordDetector(["skippidi"]), NotDetector(KeyWordDetector(["something", "not", "there"]))], False),
])
def test_and_detector(answer: str, detectors: list[Detector], detection: bool):
    detector = AndDetector(detectors)
    assert detector.detect(answer) == detection

@pytest.mark.parametrize("answer, detectors, detection", [
    ("This is just an answer", [KeyWordDetector(["just"]), KeyWordDetector(["not", "to", "be", "found"])], True),
    ("This is just an answer", [KeyWordDetector(["nothing"]), KeyWordDetector(["here"])], False),
    ("This is just an answer", [KeyWordDetector(["skippidi"]), NotDetector(KeyWordDetector(["something", "not", "there"]))], True),
])
def test_or_detector(answer: str, detectors: list[Detector], detection: bool):
    detector = OrDetector(detectors)
    assert detector.detect(answer) == detection