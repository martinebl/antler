import json
import logging
from datetime import datetime
from llmtest.attempt import Attempt

class LogWriter():
    def __init__(self):
        self.initLoggers()
    
    def initLoggers(self):
        # create loggers
        self.attempt_logger = logging.getLogger("attempt_logger")
        self.report_logger = logging.getLogger("report_logger")
        self.attempt_logger.setLevel(logging.INFO)
        self.report_logger.setLevel(logging.INFO)

        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # create file handlers
        attempt_file_handler = logging.FileHandler(f"attempts_{current_datetime}.json")
        report_file_handler = logging.FileHandler(f"report_{current_datetime}.log")

        # create formatters
        formatter = logging.Formatter('%(message)s')
        attempt_file_handler.setFormatter(formatter)
        report_file_handler.setFormatter(formatter)

        # adds handler to appropriate logger
        self.attempt_logger.addHandler(attempt_file_handler)
        self.report_logger.addHandler(report_file_handler)

    def logAttempts(self, attempts: list[Attempt]):
        self.attempt_logger.info(json.dumps(attempts, default=lambda obj: Attempt.toJSON(obj), indent=4))

    def logAttempt(self, attempt: Attempt):
        self.attempt_logger.info(json.dumps(attempt, default=lambda obj: obj.__dict__, indent=4))

    def logReport(self, report: str):
        self.report_logger.info(report)

