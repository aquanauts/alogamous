from alogamous import analyzer


class ErrorCounterAnalyzer(analyzer.Analyzer):
    def __init__(self):
        self.lines = []
        self.error_number = 0

    def read_log_line(self, line):
        self.lines.append(line)
        if "ERROR" in line:
            self.error_number += 1

    def report(self, out_stream):
        out_stream.write("There are " + str(self.error_number) + " error lines in this log")
