import io

from alogamous import analyzer, line_count_analyzer


def test_line_count():
    in_stream = io.StringIO("""line1
        line2""")
    out_stream = io.StringIO()
    analyzer.analyze_log_stream([line_count_analyzer.LineCountAnalyzer()], in_stream, out_stream)
    assert out_stream.getvalue() == "Number of log lines: 2"
