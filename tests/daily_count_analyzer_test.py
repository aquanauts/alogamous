import io

from alogamous import daily_count_analyzer, log_line_parser


def test_increase_in_info():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    comparer = daily_count_analyzer.DailyCountAnalyzer(line_parser)
    in_stream = """====================================================
STARTING Tracking service
    Start time: 2024-06-20 09:00:00.001550+00:00
    Version: 2729a
    Command line: ['.venv/bin/python3', '-m', 'app.tracking_service', '--market', 'US', '--version', '2729a']
====================================================
2024-06-20 11:00:17,983 - root - INFO - Adding subscription for pid None
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
        == """Daily increases in info log message for Tracking service:
- On 2024-06-21, the number of info messages increased by 1 from the previous day
- On 2024-06-22, the number of info messages increased by 1 from the previous day"""
    )


def test_increase_in_warning():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    comparer = daily_count_analyzer.DailyCountAnalyzer(line_parser)
    in_stream = """====================================================
STARTING Tracking service
    Start time: 2024-06-20 09:00:00.001550+00:00
    Version: 2729a
    Command line: ['.venv/bin/python3', '-m', 'app.tracking_service', '--market', 'US', '--version', '2729a']
====================================================
2024-06-20 11:40:43,527 - root - WARNING - instrument not found for sedol BYP321337
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
        == """Daily increases in warning log message for Tracking service:
- On 2024-06-21, the number of warning messages increased by 1 from the previous day
- On 2024-06-22, the number of warning messages increased by 1 from the previous day"""
    )


def test_increase_in_error():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    comparer = daily_count_analyzer.DailyCountAnalyzer(line_parser)
    in_stream = """====================================================
STARTING Tracking service
    Start time: 2024-06-20 09:00:00.001550+00:00
    Version: 2729a
    Command line: ['.venv/bin/python3', '-m', 'app.tracking_service', '--market', 'US', '--version', '2729a']
====================================================
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
        == """Daily increases in error log message for Tracking service:
- On 2024-06-21, the number of error messages increased by 1 from the previous day
- On 2024-06-22, the number of error messages increased by 1 from the previous day"""
    )


def test_mixed_increase():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    comparer = daily_count_analyzer.DailyCountAnalyzer(line_parser)
    in_stream = """====================================================
STARTING Tracking service
    Start time: 2024-06-20 09:00:00.001550+00:00
    Version: 2729a
    Command line: ['.venv/bin/python3', '-m', 'app.tracking_service', '--market', 'US', '--version', '2729a']
====================================================
2024-06-20 11:00:17,983 - root - INFO - Adding subscription for pid None
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
        == """Daily increases in info log message for Tracking service:
- On 2024-06-21, the number of info messages increased by 1 from the previous day
- On 2024-06-22, the number of info messages increased by 1 from the previous day
Daily increases in warning log message for Tracking service:
- On 2024-06-21, the number of warning messages increased by 1 from the previous day
- On 2024-06-22, the number of warning messages increased by 1 from the previous day
Daily increases in error log message for Tracking service:
- On 2024-06-21, the number of error messages increased by 1 from the previous day
- On 2024-06-22, the number of error messages increased by 1 from the previous day"""
    )


def test_no_increase():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    comparer = daily_count_analyzer.DailyCountAnalyzer(line_parser)
    in_stream = """====================================================
STARTING Tracking service
    Start time: 2024-06-20 09:00:00.001550+00:00
    Version: 2729a
    Command line: ['.venv/bin/python3', '-m', 'app.tracking_service', '--market', 'US', '--version', '2729a']
====================================================
2024-06-20 11:00:17,983 - root - INFO - Adding subscription for pid None
2024-06-20 11:40:43,527 - root - WARNING - instrument not found for sedol BYP321337
2024-06-20 17:16:03,660 - root - ERROR - Caught exception N/A. Message: Unclosed client session
2024-06-21 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-21 11:40:43,527 - root - WARNING - Could not find instrument for sedol BYP321337, trying ric YT.ATS
2024-06-21 17:25:08,029 - root - ERROR - Exception in message handler"""
    out_stream = io.StringIO()
    for line in in_stream.splitlines():
        comparer.read_log_line(line)
    comparer.report(out_stream)
    assert out_stream.getvalue() == ""


def test_other_format():
    line_parser = log_line_parser.LogLineParser(
        [["datetime", "thread", "level", "source"], ["message"]],
        " - ",
        "====================================================",
        " ",
    )
    comparer = daily_count_analyzer.DailyCountAnalyzer(line_parser)
    in_stream = """====================================================
STARTING PROCESS Java Price Process
    Start time: 2024-06-27 12:00:00.060562+00:00
    Version: 2757
    Command line: ['./build/app/java_process', '--market', 'US']
====================================================
2024-06-27T12:00:00.460+0000 [main] WARN com.app.java_process.info - Starting with config
2024-06-28T12:00:00.693+0000 [main] WARN com.app.java_process.info - Reading from kafka servers brokers:9092
2024-06-28T12:00:00.745+0000 [main] WARN com.app.java_process.info - Reading topic java_topic from kafka servers
2024-06-28T12:00:00.745+0000 [main] WARN com.app.java_process.info - Reading messages for 2024-06-27"""
    out_stream = io.StringIO()
    for line in in_stream.splitlines():
        comparer.read_log_line(line)
    comparer.report(out_stream)
    assert (
        out_stream.getvalue()
        == """Daily increases in warning log message for PROCESS Java Price Process:
- On 2024-06-28, the number of warning messages increased by 2 from the previous day"""
    )


def test_multiple_services():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    comparer = daily_count_analyzer.DailyCountAnalyzer(line_parser)
    in_stream = """====================================================
STARTING Tracking service
    Start time: 2024-06-20 09:00:00.001550+00:00
    Version: 2729a
    Command line: ['.venv/bin/python3', '-m', 'app.tracking_service', '--market', 'US', '--version', '2729a']
====================================================
2024-06-20 11:00:17,983 - root - INFO - Adding subscription for pid None
2024-06-21 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-21 11:00:18,115 - root - INFO - Scheduling Error Handler in 150.0 seconds
====================================================
STARTING PROCESS Quantity Loader
    Start time: 2024-05-30 10:30:00.034654+00:00
    Version: 2673
    Command line: ['.venv/bin/python3', '-m', 'loaders.quantity_loader', '--market', 'US']
====================================================
2024-05-30 10:30:18,446 - root - INFO - prometheus client http server running on http://prometheus.co
2024-05-31 10:30:18,549 - root - INFO - Initialized prometheus server.
2024-05-31 10:30:18,549 - root - INFO - Kafka publishing on topic topic_internal at brokers:9092"""
    out_stream = io.StringIO()
    for line in in_stream.splitlines():
        comparer.read_log_line(line)
    comparer.report(out_stream)
    assert (
        out_stream.getvalue()
        == """Daily increases in info log message for Tracking service:
- On 2024-06-21, the number of info messages increased by 1 from the previous day
Daily increases in info log message for PROCESS Quantity Loader:
- On 2024-05-31, the number of info messages increased by 1 from the previous day"""
    )


def test_same_service():
    line_parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    comparer = daily_count_analyzer.DailyCountAnalyzer(line_parser)
    in_stream = """====================================================
STARTING Tracking service
    Start time: 2024-06-20 09:00:00.001550+00:00
    Version: 2729a
    Command line: ['.venv/bin/python3', '-m', 'app.tracking_service', '--market', 'US', '--version', '2729a']
====================================================
2024-06-20 11:00:17,983 - root - INFO - Adding subscription for pid None
2024-06-21 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-21 11:00:18,115 - root - INFO - Scheduling Error Handler in 150.0 seconds
====================================================
STARTING Tracking service
    Start time: 2024-06-20 09:00:00.001550+00:00
    Version: 2729a
    Command line: ['.venv/bin/python3', '-m', 'app.tracking_service', '--market', 'US', '--version', '2729a']
====================================================
2024-05-30 10:30:18,446 - root - INFO - prometheus client http server running on http://prometheus.co
2024-05-31 10:30:18,549 - root - INFO - Initialized prometheus server.
2024-05-31 10:30:18,549 - root - INFO - Kafka publishing on topic topic_internal at brokers:9092"""
    out_stream = io.StringIO()
    for line in in_stream.splitlines():
        comparer.read_log_line(line)
    comparer.report(out_stream)
    assert (
        out_stream.getvalue()
        == """Daily increases in info log message for Tracking service:
- On 2024-05-31, the number of info messages increased by 1 from the previous day
- On 2024-06-21, the number of info messages increased by 1 from the previous day"""
    )
