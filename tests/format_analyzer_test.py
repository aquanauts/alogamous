from io import StringIO

from alogamous import format_analyzer, log_line_parser


def test_format_analyzer():
    parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    format_checker = format_analyzer.FormatAnalyzer(parser)
    in_stream = """====================================================
STARTING Tracking service
    Start time: 2024-06-20 09:00:00.001550+00:00
    Version: 2729a
    Command line: ['.venv/bin/python3', '-m', 'app.tracking_service', '--market', 'US', '--version', '2729a']
====================================================
2024-06-20 11:00:17,983 - root - INFO - Adding subscription for pid None
Hello I am a bad log line
2024-06-20 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-20 11:00:18,115 - root - INFO - Scheduling Error Handler in 150.0 seconds
2024-06-20 11:00:18,116 - root - INFO - prometheus client http server running
Hello I am a bad log line"""
    out_stream = StringIO()
    for line in in_stream.splitlines():
        format_checker.read_log_line(line)
    format_checker.report(out_stream)
    assert (
        out_stream.getvalue()
        == """Lines that do not conform to log format:
- Hello I am a bad log line
- Hello I am a bad log line"""
    )
