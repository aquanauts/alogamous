import io

from alogamous import error_counter_analyzer, log_line_parser


def test_error_counter():
    parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    counter = error_counter_analyzer.ErrorCounterAnalyzer(parser)
    in_stream = io.StringIO(
        """2024-06-20 17:16:03,660 - root - ERROR - Caught exception N/A.
2024-06-20 17:16:03,660 - root - ERROR - Caught exception N/A. Message: Unclosed connector NoneType: None"""
    )
    out_stream = io.StringIO()
    for line in in_stream:
        counter.read_log_line(line)
    counter.report(out_stream)
    assert out_stream.getvalue().strip() == "Number of error lines: 2"


def test_no_errors():
    parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    counter = error_counter_analyzer.ErrorCounterAnalyzer(parser)
    in_stream = io.StringIO("""2024-06-20 17:17:04,278 - root - INFO - Updating prices
2024-06-20 17:24:34,091 - root - INFO - Closing client connection.""")
    out_stream = io.StringIO()
    for line in in_stream:
        counter.read_log_line(line)
    counter.report(out_stream)
    assert out_stream.getvalue().strip() == "Number of error lines: 0"


def test_no_input_lines():
    parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    counter = error_counter_analyzer.ErrorCounterAnalyzer(parser)
    out_stream = io.StringIO()
    counter.report(out_stream)
    assert out_stream.getvalue().strip() == "Number of error lines: 0"
