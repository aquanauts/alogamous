from alogamous import analyzer


class FlagDuplicateLogMessages(analyzer.Analyzer):
    def __init__(self):
        self.logMessages = set()
        self.duplicateMessages = set()

    def read_log_line(self, line):
        message = line.split("-")[-1].strip()
        if message in self.logMessages:
            self.duplicateMessages.add(message)
        else:
            self.logMessages.add(message)

    def report(self, out_stream):
        if len(self.duplicateMessages) > 0:
            out_stream.write("Duplicate Log Messages:\n")
            out_stream.write("\n".join(self.duplicateMessages))
        else:
            out_stream.write("No duplicate log messages")
