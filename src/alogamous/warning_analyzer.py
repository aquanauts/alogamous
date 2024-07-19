from alogamous import analyzer


class WarningAnalyzer(analyzer.Analyzer):
    def __init__(self):
        self.count = 0

    def read_log_line(self, line):
        line_list = line.split(" ")
        # List should have format [date, timestamp, -, root, -, log message type, -, first word of message...]
        if line_list[5].lower() == "warning":
            self.count += 1

    def report(self, out_stream):
        if self.count == 0:
            out_stream.write("\n" + "No Warnings were detected.")
        elif self.count == 1:
            out_stream.write("\n" + "1 Warning was detected.")
        else:
            out_stream.write("\n" + str(self.count) + " Warnings were detected.")
