import io

from alogamous import analyzer


class TestAnalyzer1(analyzer.Analyzer):
    def read_log_line(self, line):
        pass

    def report(self, out_stream):
        pass


class TestAnalyzer2(analyzer.Analyzer):
    def read_log_line(self, line):
        pass

    def report(self, out_stream):
        pass


def test_analyze_log_stream():
    in_stream = io.StringIO("""line1
            line2
            line3""")
    out_stream = io.StringIO()

    analyzer.analyze_log_stream([TestAnalyzer1(), TestAnalyzer2()], in_stream, out_stream)
    assert out_stream.getvalue() == "\n\n\n\n>>>>>>>>>> a report has been reported <<<<<<<<<<\n\n"
