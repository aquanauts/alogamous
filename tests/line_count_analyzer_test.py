import io

from alogamous.line_count_analyzer import LineCountAnalyzer


def test_report():
    log_line_counter = LineCountAnalyzer()
    out_stream = io.StringIO()

    log_line_counter.read_log_line(log_line_counter)
    log_line_counter.read_log_line(log_line_counter)
    log_line_counter.report(out_stream)
    assert out_stream.getvalue() == "Number of log lines: 2"


def test_report_without_readline():
    log_line_counter = LineCountAnalyzer()
    out_stream = io.StringIO()
    log_line_counter.report(out_stream)
    assert out_stream.getvalue() == "Number of log lines: 0"
