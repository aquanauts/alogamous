import io

from alogamous import log_line_parser, startup_header_analyzer


def test_report():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    startup_analyzer = startup_header_analyzer.StartupHeaderAnalyzer(line_parser)
    in_stream = """====================================================
STARTING Tracking service
    Start time: 2024-06-20 09:00:00.001550+00:00
    Version: 2729a
    Command line: ['.venv/bin/python3', '-m', 'app.tracking_service', '--market', 'US', '--version', '2729a']
====================================================
2024-06-20 11:00:17,983 - root - INFO - Adding subscription for pid None
2024-06-20 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-20 11:00:18,115 - root - INFO - Scheduling Error Handler in 150.0 seconds"""
    out_stream = io.StringIO()
    for line in in_stream.splitlines():
        startup_analyzer.read_log_line(line)
    startup_analyzer.report(out_stream)
    assert (
        out_stream.getvalue()
        == """
Lines that are part of the startup header(s):
- STARTING Tracking service
-     Start time: 2024-06-20 09:00:00.001550+00:00
-     Version: 2729a
-     Command line: ['.venv/bin/python3', '-m', 'app.tracking_service', '--market', 'US', '--version', '2729a']"""
    )
