from alogamous import analyzer, log_line_parser


class WarningAnalyzer(analyzer.Analyzer):
    def __init__(self, line_parser):
        self.parser = line_parser
        self.count = 0

    def read_log_line(self, line):
        parsed_line = self.parser.parse(line)
        if parsed_line["type"] == log_line_parser.LineType.LOG_LINE and parsed_line["level"].lower().startswith("warn"):
            self.count += 1

    def report(self, out_stream):
        if self.count == 0:
            out_stream.write("No Warnings were detected.")
        elif self.count == 1:
            out_stream.write("1 Warning was detected.")
        else:
            out_stream.write(str(self.count) + " Warnings were detected.")
