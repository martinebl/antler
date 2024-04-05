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
        self.attempt_file_path = f"logs/attempts_{current_datetime}.json"
        report_file_handler = logging.FileHandler(f"reports/report_{current_datetime}.log")

        # create formatters
        formatter = logging.Formatter('%(message)s')
        # attempt_file_handler.setFormatter(formatter)
        report_file_handler.setFormatter(formatter)

        # adds handler to appropriate logger
        # self.attempt_logger.addHandler(attempt_file_handler)
        self.report_logger.addHandler(report_file_handler)

    
    def logTransformAttempts(self, attempts: list[Attempt]):
        """
        Appends the list of attempts from a single transform, to the attempts.json file
        To avoid parsing the whole json file, and rewrite it all, some string manipulation is required
        """
        with open(self.attempt_file_path, 'rb+') as file:
            file.seek(-9, 2)
            for attempt in attempts:
                json_str = json.dumps(Attempt.toJSON(attempt), indent=4)
                # Fix the base indentation
                indented = [(" " * 8) + line for line in json_str.splitlines()]
                file.write("\n".join(indented).encode())
                file.write(b",\n")
            # End the file properly
            file.write(b"\n    ]\n}\n")

    def fixAttemptFileEnding(self):
        """
        Remove the trailing comma, and extra newline at the end
        """
        with open(self.attempt_file_path, "rb+") as file:
            file.seek(-11, 2)
            file.write(b"\n    ]\n}\n\n")
            file.seek(0, 2)
            size = file.tell()
            file.truncate(size - 2)

    def logReport(self, report: str):
        self.report_logger.info(f'{self.run_params["generator_type"]}: {self.run_params["model"]}')
        self.report_logger.info(report)

    def LogRunParams(self, params: dict):
        self.run_params = params
        # Hardcoded json for logging the params, with an attempt array with whitespace
        with open(self.attempt_file_path, "w") as file:
            file.write("{\n")
            for (key, value) in self.run_params.items():
                file.write(f"    \"{key}\": {json.dumps(value)},\n")
            file.write("    \"attempts\": [\n   ]\n}\n")

