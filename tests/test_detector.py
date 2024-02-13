import pytest
from llmtest.detector import Detector

@pytest.fixture
def targets():
    return ["Test", "test", "Target", "target"]

def test_detect_targets(targets):
    detector = Detector(targets)
    assert detector.detectTargets(''.join(targets))