from llmtest.logwriter import LogWriter
from llmtest.attempt import Attempt
from llmtest.transforms import Transform
from llmtest.techniques.acceptingprefix import AcceptingPrefix
from llmtest.probes.buildabomb import BuildABomb
import json



def test_logwriter():
    log_writer = LogWriter()
    log_writer.LogRunParams({
        "generator_type": "Testing type",
        "model": "Test model",
        "model_options": {},
        "repetitions": 1,
    })
    attempt = Attempt(Transform([(1, AcceptingPrefix())]), BuildABomb())
    log_writer.logTransformAttempts([attempt])
    log_writer.logTransformAttempts([attempt])
    log_writer.fixAttemptFileEnding()
    try:
        with open(log_writer.attempt_file_path, 'r') as file:
            json.load(file)
        assert True
    except json.JSONDecodeError:
        assert False