import io

from alogamous.daily_warning_analyzer import DailyWarningAnalyzer
from alogamous.log_line_parser import LogLineParser


def test_daily_warning_analyzer():
    daily_warning_analyzer = DailyWarningAnalyzer(
        LogLineParser(["datetime", "source", "level", "message"], " - ", "HEADER")
    )
    out_stream = io.StringIO()

    daily_warning_analyzer.read_log_line("HEADER")
    daily_warning_analyzer.read_log_line("2024-06-20 17:24:34,092 - root - INFO - Adding subscription for pid None")
    daily_warning_analyzer.read_log_line("2024-06-20 11:40:43,529 - root - WARNING - instrument not found")
    daily_warning_analyzer.read_log_line("2024-06-21 11:00:17,983 - root - INFO - Initialized Influx DB Client to host")
    daily_warning_analyzer.read_log_line("2024-06-21 11:40:43,529 - root - WARNING - instrument not found")
    daily_warning_analyzer.report(out_stream)

    assert out_stream.getvalue() == """Daily warning messages:\ninstrument not found\n"""


def test_no_daily_warnings():
    daily_warning_analyzer = DailyWarningAnalyzer(
        LogLineParser(["datetime", "source", "level", "message"], " - ", "HEADER")
    )
    out_stream = io.StringIO()

    daily_warning_analyzer.read_log_line("HEADER")
    daily_warning_analyzer.read_log_line("2024-06-20 17:24:34,092 - root - INFO - Message 1")
    daily_warning_analyzer.read_log_line("2024-06-20 11:40:43,529 - root - WARNING - Message 2")
    daily_warning_analyzer.read_log_line("2024-06-21 11:00:17,983 - root - INFO - Message 3")
    daily_warning_analyzer.report(out_stream)

    assert out_stream.getvalue() == """There are no daily warning messages.\n"""


def test_multiple_daily_warnings():
    daily_warning_analyzer = DailyWarningAnalyzer(
        LogLineParser(["datetime", "source", "level", "message"], " - ", "HEADER")
    )
    out_stream = io.StringIO()

    daily_warning_analyzer.read_log_line("HEADER")
    daily_warning_analyzer.read_log_line("2024-06-20 17:24:34,092 - root - INFO - Message 1")
    daily_warning_analyzer.read_log_line("2024-06-20 11:40:43,529 - root - WARNING - Message 2")
    daily_warning_analyzer.read_log_line("2024-06-21 11:00:17,983 - root - INFO - Message 3")
    daily_warning_analyzer.read_log_line("2024-06-21 11:00:17,983 - root - WARNING - Message 4")
    daily_warning_analyzer.read_log_line("2024-06-21 11:40:43,529 - root - WARNING - Message 2")
    daily_warning_analyzer.read_log_line("2024-06-22 11:00:17,983 - root - WARNING - Message 4")
    daily_warning_analyzer.report(out_stream)

    assert out_stream.getvalue() == """Daily warning messages:\nMessage 2\nMessage 4\n"""
