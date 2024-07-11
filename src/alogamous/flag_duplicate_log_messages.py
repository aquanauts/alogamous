from alogamous import analyzer


class FlagDuplicateLogMessages(analyzer.Analyzer):
    def __init__(self):
        self.logMessages = []
        self.duplicateMessages = set()

    def read_log_line(self, line):
        message = line.split("-")[-1].strip()
        self.logMessages.append(message)

        for message in self.logMessages:
            if self.logMessages.count(message) > 1:
                self.duplicateMessages.add(message)

    def report(self, out_stream):
        out_stream.write("Duplicate Log Messages:\n")
        for message in self.duplicateMessages:
            out_stream.write(f"{message}\n")
