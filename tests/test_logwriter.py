from antler.logwriter import LogWriter
from antler.attempt import Attempt
from antler.transforms import Transform
from antler.techniques.acceptingprefix import AcceptingPrefix
from antler.probes.buildabomb import BuildABomb
import json


def test_logwriter():
    log_writer = LogWriter()
    log_writer.LogRunParams({
        "generator_type": "Testing type",
        "model": "Test model",
        "explorer": "Classexplorer",
        "model_options": {},
        "repetitions": 1,
    })
    attempt = Attempt(Transform([ AcceptingPrefix() ]), BuildABomb())
    log_writer.logTransformAttempts([attempt])
    log_writer.logTransformAttempts([attempt])
    log_writer.fixAttemptFileEnding()
    log_writer.logReport("something")
    try:
        with open(log_writer.attempt_file_path, 'r') as file:
            json.load(file)
        assert True
    except json.JSONDecodeError:
        assert False