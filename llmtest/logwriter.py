import json
import os
import logging
from datetime import datetime
from llmtest.attempt import Attempt

class LogWriter():
    def __init__(self):
        self.initLoggers()
    
    def initLoggers(self):
        # check dirs exist
        if not os.path.exists('logs'):
            os.mkdir('logs')
        if not os.path.exists('reports'):
            os.mkdir('reports')

        self.run_params = {}

        # create loggers
        self.attempt_logger = logging.getLogger("attempt_logger")
        self.report_logger = logging.getLogger("report_logger")
        self.attempt_logger.setLevel(logging.INFO)
        self.report_logger.setLevel(logging.INFO)

        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # create file handlers
        attempt_file_handler = logging.FileHandler(f"logs/attempts_{current_datetime}.json")
        report_file_handler = logging.FileHandler(f"reports/report_{current_datetime}.log")

        # create formatters
        formatter = logging.Formatter('%(message)s')
        attempt_file_handler.setFormatter(formatter)
        report_file_handler.setFormatter(formatter)

        # adds handler to appropriate logger
        self.attempt_logger.addHandler(attempt_file_handler)
        self.report_logger.addHandler(report_file_handler)

    def logAttempts(self, attempts: list[Attempt]):
        attempts_as_dict = [Attempt.toJSON(attempt) for attempt in attempts]
        self.run_params["attempts"] = attempts_as_dict
        self.attempt_logger.info(json.dumps(self.run_params, indent=4))

    def logReport(self, report: str):
        self.report_logger.info(f'{self.run_params["generator_type"]}: {self.run_params["model"]}')
        self.report_logger.info(report)

    def setLogRunParams(self, params: object):
        self.run_params = params

