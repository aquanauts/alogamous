import io
from alogamous import analyzer


class EchoAnalyzer(analyzer.Analyzer):
    def __init__(self):
        self.lines = []

    def read_log_line(self, line):
        self.lines.append(line)

    def report(self, out_stream):
        out_stream.write("\n".join(self.lines))


def test_echo_lines():
    in_stream = io.StringIO("""line1
        line2
        line3""")
    out_stream = io.StringIO()
    analyzer.analyze_log_stream([EchoAnalyzer()], in_stream, out_stream)
    assert out_stream.getvalue() == """line1
        line2
        line3"""
