import io

from alogamous import analyzer, flag_duplicate_log_messages


def test_flag_duplicate_log_messages():
    in_stream = io.StringIO("""Date - root - INFO - log message 1
        Date - root - WARNING - log message 2
        Date - root - WARNING - log message 1""")
    out_stream = io.StringIO()
    analyzer.analyze_log_stream([flag_duplicate_log_messages.FlagDuplicateLogMessages()], in_stream, out_stream)
    assert (
        out_stream.getvalue()
        == """ Duplicate log messages:
        log message 1"""
    )
