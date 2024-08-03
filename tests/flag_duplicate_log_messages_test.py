import io

from alogamous import flag_duplicate_log_messages


def test_flag_duplicate_log_messages():
    flagger = flag_duplicate_log_messages.FlagDuplicateLogMessages()
    in_stream = io.StringIO("""Date - root - INFO - log message 1
        Date - root - WARNING - log message 2
        Date - root - WARNING - log message 1""")
    out_stream = io.StringIO()
    for line in in_stream:
        flagger.read_log_line(line)
    flagger.report(out_stream)
    assert out_stream.getvalue() == """Duplicate Log Messages:\nlog message 1"""


def test_flag_duplicate_log_messages_no_duplicates():
    flagger = flag_duplicate_log_messages.FlagDuplicateLogMessages()
    in_stream = io.StringIO("""Date - root - INFO - log message 1
        Date - root - WARNING - log message 2
        Date - root - WARNING - log message 3""")
    out_stream = io.StringIO()
    for line in in_stream:
        flagger.read_log_line(line)
    flagger.report(out_stream)
    assert out_stream.getvalue() == """No duplicate log messages"""
