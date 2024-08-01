import io

from alogamous import daily_count_analyzer, log_line_parser


def test_increase_in_info():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    comparer = daily_count_analyzer.DailyCountAnalyzer(line_parser)
    in_stream = """2024-06-20 11:00:17,983 - root - INFO - Adding subscription for pid None
2024-06-21 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-21 11:00:17,983 - root - INFO - Adding subscription for pid None
2024-06-22 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-22 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-22 11:00:18,115 - root - INFO - Initialized Influx DB Client to host"""
    out_stream = io.StringIO()
    for line in in_stream.splitlines():
        comparer.read_log_line(line)
    comparer.report(out_stream)
    assert (
        out_stream.getvalue()
        == """Instances where specific types of messages increased from previous day:
- Number of info messages increased by 1 on 2024-06-21
- Number of info messages increased by 1 on 2024-06-22"""
    )


def test_increase_in_warning():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    comparer = daily_count_analyzer.DailyCountAnalyzer(line_parser)
    in_stream = """2024-06-20 11:40:43,527 - root - WARNING - instrument not found for sedol BYP321337
2024-06-21 11:40:43,527 - root - WARNING - Could not find instrument for sedol BYP321337, trying ric YT.ATS
2024-06-21 11:40:43,527 - root - WARNING - instrument not found for ric YT.ATS
2024-06-22 11:40:43,527 - root - WARNING - Could not find instrument for ric YT.ATS, using provided identifier 1
2024-06-22 11:40:43,527 - root - WARNING - instrument not found for sedol DHI7337
2024-06-22 11:40:43,527 - root - WARNING - instrument not found for sedol DHI7337"""
    out_stream = io.StringIO()
    for line in in_stream.splitlines():
        comparer.read_log_line(line)
    comparer.report(out_stream)
    assert (
        out_stream.getvalue()
        == """Instances where specific types of messages increased from previous day:
- Number of warning messages increased by 1 on 2024-06-21
- Number of warning messages increased by 1 on 2024-06-22"""
    )


def test_increase_in_error():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    comparer = daily_count_analyzer.DailyCountAnalyzer(line_parser)
    in_stream = """2024-06-20 17:16:03,660 - root - ERROR - Caught exception N/A. Message: Unclosed client session
2024-06-21 17:16:03,660 - root - ERROR - Caught exception N/A. Message: Unclosed connector NoneType: None
2024-06-21 17:25:08,029 - root - ERROR - Exception in message handler
2024-06-22 17:16:03,660 - root - ERROR - Caught exception N/A. Message: Unclosed connector NoneType: None
2024-06-22 17:25:08,029 - root - ERROR - Exception in message handler
2024-06-22 17:25:08,029 - root - ERROR - Exception in message handler"""
    out_stream = io.StringIO()
    for line in in_stream.splitlines():
        comparer.read_log_line(line)
    comparer.report(out_stream)
    assert (
        out_stream.getvalue()
        == """Instances where specific types of messages increased from previous day:
- Number of error messages increased by 1 on 2024-06-21
- Number of error messages increased by 1 on 2024-06-22"""
    )


def test_mixed_increase():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    comparer = daily_count_analyzer.DailyCountAnalyzer(line_parser)
    in_stream = """2024-06-20 11:00:17,983 - root - INFO - Adding subscription for pid None
2024-06-21 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-21 11:00:17,983 - root - INFO - Adding subscription for pid None
2024-06-22 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-22 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-22 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-20 11:40:43,527 - root - WARNING - instrument not found for sedol BYP321337
2024-06-21 11:40:43,527 - root - WARNING - Could not find instrument for sedol BYP321337, trying ric YT.ATS
2024-06-21 11:40:43,527 - root - WARNING - instrument not found for ric YT.ATS
2024-06-22 11:40:43,527 - root - WARNING - Could not find instrument for ric YT.ATS, using provided identifier 1
2024-06-22 11:40:43,527 - root - WARNING - instrument not found for sedol DHI7337
2024-06-22 11:40:43,527 - root - WARNING - instrument not found for sedol DHI7337
2024-06-20 17:16:03,660 - root - ERROR - Caught exception N/A. Message: Unclosed client session
2024-06-21 17:16:03,660 - root - ERROR - Caught exception N/A. Message: Unclosed connector NoneType: None
2024-06-21 17:25:08,029 - root - ERROR - Exception in message handler
2024-06-22 17:16:03,660 - root - ERROR - Caught exception N/A. Message: Unclosed connector NoneType: None
2024-06-22 17:25:08,029 - root - ERROR - Exception in message handler
2024-06-22 17:25:08,029 - root - ERROR - Exception in message handler"""
    out_stream = io.StringIO()
    for line in in_stream.splitlines():
        comparer.read_log_line(line)
    comparer.report(out_stream)
    assert (
        out_stream.getvalue()
        == """Instances where specific types of messages increased from previous day:
- Number of info messages increased by 1 on 2024-06-21
- Number of info messages increased by 1 on 2024-06-22
- Number of warning messages increased by 1 on 2024-06-21
- Number of warning messages increased by 1 on 2024-06-22
- Number of error messages increased by 1 on 2024-06-21
- Number of error messages increased by 1 on 2024-06-22"""
    )


def test_no_increase():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    comparer = daily_count_analyzer.DailyCountAnalyzer(line_parser)
    in_stream = """2024-06-20 11:00:17,983 - root - INFO - Adding subscription for pid None
2024-06-20 11:40:43,527 - root - WARNING - instrument not found for sedol BYP321337
2024-06-20 17:16:03,660 - root - ERROR - Caught exception N/A. Message: Unclosed client session
2024-06-21 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-21 11:40:43,527 - root - WARNING - Could not find instrument for sedol BYP321337, trying ric YT.ATS
2024-06-21 17:25:08,029 - root - ERROR - Exception in message handler"""
    out_stream = io.StringIO()
    for line in in_stream.splitlines():
        comparer.read_log_line(line)
    comparer.report(out_stream)
    assert out_stream.getvalue() == "Instances where specific types of messages increased from previous day:"
