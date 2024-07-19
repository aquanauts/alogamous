from alogamous import analyzer


class ErrorCounterAnalyzer(analyzer.Analyzer):
    def __init__(self):
        self.error_number = 0

    def read_log_line(self, line):
        if "ERROR" in line:
            self.error_number += 1

    def report(self, out_stream):
        out_stream.write("Number of error lines: " + str(self.error_number))
