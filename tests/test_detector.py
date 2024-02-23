import pytest
from llmtest.detectors import Detector
from llmtest.detectors.simpledetector import SimpleDetector

@pytest.fixture
def targets():
    return ["Test", "test", "Target", "target"]

def test_base_detector_not_implemented():
    with pytest.raises(NotImplementedError):
        Detector().detect("prompt")

def test_detect_targets(targets):
    detector = SimpleDetector(targets)
    assert detector.detect(''.join(targets))