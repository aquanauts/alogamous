from alogamous import analyzer, log_line_parser


class FlagDuplicateLogMessages(analyzer.Analyzer):
    def __init__(self, line_parser):
        self.parser = line_parser
        self.logMessages = set()
        self.duplicateMessages = set()

    def read_log_line(self, line):
        parsed_line = self.parser.parse(line)
        if parsed_line["type"] == log_line_parser.LineType.LOG_LINE:
            message = parsed_line["message"]
            if message in self.logMessages:
                self.duplicateMessages.add(message)
            else:
                self.logMessages.add(message)

    def report(self, out_stream):
        if len(self.duplicateMessages) > 0:
            out_stream.write("Duplicate Log Messages:\n- ")
            out_stream.write("\n- ".join(self.duplicateMessages))
        else:
            out_stream.write("No duplicate log messages")
