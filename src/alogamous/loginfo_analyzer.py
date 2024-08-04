from alogamous import analyzer
from alogamous.log_line_parser import LineType


class InfoAnalyzer(analyzer.Analyzer):
    def __init__(self, parser):
        self.infomessage_counter = 0
        self.parser = parser

    def read_log_line(self, line):
        parsed_line = self.parser.parse(line)
        line_type = parsed_line["type"]
        if line_type == LineType.LOG_LINE and parsed_line["level"].lower() == "info":
            self.infomessage_counter += 1

    def report(self, out_stream):
        out_stream.write("Number of info messages: " + str(self.infomessage_counter))
