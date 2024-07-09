from alogamous import analyzer


class LineCountAnalyzer(analyzer.Analyzer):
    def __init__(self):
        self.line_counter = 0

    def read_log_line(self, _):
        self.line_counter += 1

    def report(self, out_stream):
        out_stream.write("Number of log lines: " + str(self.line_counter))
