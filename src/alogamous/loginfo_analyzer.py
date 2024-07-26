from alogamous import analyzer


class InfoAnalyzer(analyzer.Analyzer):
    def __init__(self):
        self.infomessage_counter = 0

    def read_log_line(self, line):
        if "info" in line:
            self.infomessage_counter += 1

    def report(self, out_stream):
        out_stream.write("Number of info messages: " + str(self.infomessage_counter))
