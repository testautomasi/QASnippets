from robot.api import ResultVisitor
from collections import defaultdict
from datetime import datetime
import threading


class CustomReportListener(ResultVisitor):

    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, output="error_report.html"):
        # Dictionary to store exception details
        self.test_details = defaultdict(lambda: {"error_count": 0, "latest_test": None})
        self.output = output
        self.lock = threading.Lock()

    def start_suite(self, name, result):
        pass

    def end_suite(self, name, result):
        pass

    def start_test(self, name, result):
        pass

    def end_test(self, name, result):
        if not result.passed:
            error_message = result.message
            with self.lock:
                if error_message not in self.test_details:
                    self.test_details[error_message] = {
                        "error_count": 0,
                        "latest_test": "",
                    }
                self.test_details[error_message]["error_count"] += 1
                self.test_details[error_message]["latest_test"] = result.name

    def close(self):
        self._generate_html_report()

    def _generate_html_report(self):
        with self.lock:
            with open(self.output, "w") as f:
                f.write("<html><head><title>Test Error Report</title></head><body>\n")
                f.write("<h1>Test Error Report</h1>\n")
                f.write(f"<p>Generated on {datetime.now()}</p>\n")
                f.write("<table border='1'>\n")
                f.write(
                    "<tr><th>Error Message</th><th>Error Count</th><th>Latest Test</th></tr>\n"
                )
                for error_message, details in self.test_details.items():
                    f.write(
                        f"<tr><td>{error_message}</td><td>{details['error_count']}</td><td>{details['latest_test']}</td></tr>\n"
                    )
                f.write("</table>\n")
                f.write("</body></html>\n")
