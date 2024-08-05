import io

from alogamous import flag_duplicate_log_messages, log_line_parser


def test_flag_duplicate_log_messages():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    flagger = flag_duplicate_log_messages.FlagDuplicateLogMessages(line_parser)
    in_stream = io.StringIO("""Date - root - INFO - log message 1
        Date - root - WARNING - log message 2
        Date - root - WARNING - log message 1""")
    out_stream = io.StringIO()
    for line in in_stream:
        flagger.read_log_line(line.rstrip())
    flagger.report(out_stream)
    assert out_stream.getvalue() == """Duplicate Log Messages:\n- log message 1"""


def test_flag_duplicate_log_messages_no_duplicates():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    flagger = flag_duplicate_log_messages.FlagDuplicateLogMessages(line_parser)
    in_stream = io.StringIO("""Date - root - INFO - log message 1
        Date - root - WARNING - log message 2
        Date - root - WARNING - log message 3""")
    out_stream = io.StringIO()
    for line in in_stream:
        flagger.read_log_line(line.rstrip())
    flagger.report(out_stream)
    assert out_stream.getvalue() == """No duplicate log messages"""


def test_flag_duplicate_messages_with_header_and_dashes():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    flagger = flag_duplicate_log_messages.FlagDuplicateLogMessages(line_parser)
    in_stream = io.StringIO("""====================================================
STARTING Tracking service
    Start time: 2024-06-20 09:00:00.001550+00:00
    Version: 2729a
    Command line: ['.venv/bin/python3', '-m', 'app.tracking_service', '--market', 'US', '--version', '2729a']
====================================================
2024-06-20 11:00:17,983 - root - INFO - Adding subscription for pid None
2024-06-20 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-20 11:00:18,185 - root - INFO - Kafka reading from start of day 2024-06-20 05:00:00+00:00 on topic internal""")
    out_stream = io.StringIO()
    for line in in_stream:
        flagger.read_log_line(line.rstrip())
    flagger.report(out_stream)
    assert out_stream.getvalue() == """No duplicate log messages"""
