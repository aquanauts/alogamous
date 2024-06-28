from alogamous import analyzer


class EchoAnalyzer(analyzer.Analyzer):
    def __init__(self):
        self.lines = []

    def read_log_line(self, line):
        self.lines.append(line)

    def report(self, out_stream):
        out_stream.write("\n".join(self.lines))
