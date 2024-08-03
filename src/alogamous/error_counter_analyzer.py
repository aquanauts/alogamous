from alogamous import analyzer, log_line_parser


class ErrorCounterAnalyzer(analyzer.Analyzer):
    def __init__(self, line_parser):
        self.parser = line_parser
        self.error_number = 0

    def read_log_line(self, line):
        parsed_line = self.parser.parse(line)
        if parsed_line["type"] == log_line_parser.LineType.LOG_LINE and parsed_line["level"].lower() == "error":
            self.error_number += 1

    def report(self, out_stream):
        out_stream.write("Number of error lines: " + str(self.error_number))
