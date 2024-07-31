from io import StringIO

from alogamous import format_analyzer, log_line_parser


def test_format_analyzer_with_bad_lines():
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
        == """
Lines that do not conform to log format:
- Hello I am a bad log line
- Hello I am a bad log line"""
    )


def test_format_analyzer_with_good_lines():
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
    2024-06-20 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
    2024-06-20 11:00:18,115 - root - INFO - Scheduling Error Handler in 150.0 seconds
    2024-06-20 11:00:18,116 - root - INFO - prometheus client http server running"""
    out_stream = StringIO()
    for line in in_stream.splitlines():
        format_checker.read_log_line(line)
    format_checker.report(out_stream)
    assert out_stream.getvalue() == "All lines conform to log line format"


def test_format_with_stack_trace():
    parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    format_checker = format_analyzer.FormatAnalyzer(parser)
    in_stream = """2024-07-23 21:13:53,862 - root - INFO - Closing client connection.
Hello I am a bad log line
2024-07-23 21:13:53,862 - root - INFO - Closing client connection.
Traceback (most recent call last):
  File "<frozen runpy>", line 1938, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File ".build/2811/execution/execution_service", line 973, in <module>
    app.run(life_cycle_runner.run, life_cycle_runner.stop)
  File ".build/2811/app/application.py", line 219, in run
    run(self.start(my_date, main, stop))
  File ".build/2811/.venv/lib/python3.11/runners.py", line 190, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File ".build/2811/.venv/lib/python3.11/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".build/2811/.venv/lib/python3.11/events.py", line 653, in run_until_done
    return future.result()
           ^^^^^^^^^^^^^^^
  File "2811/app/application.py", line 421, in start
    await self.task
  File "2811/messages/app/runner.py", line 449, in run
    await asyncio.gather(*self.running_tasks)
  File "2811/messages/processor.py", line 340, in run
    await self.dispatch(message)
  File ".build/2811/execution/execution_service", line 1315, in market_test
    if symbol and obj.region != 'NORTHAMERICA'
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'region'
2024-07-23 21:13:53,862 - root - INFO - Closing client connection.
Hello I am a bad log line"""
    out_stream = StringIO()
    for line in in_stream.splitlines():
        format_checker.read_log_line(line)
    format_checker.report(out_stream)
    assert (
        out_stream.getvalue()
        == """
Lines that do not conform to log format:
- Hello I am a bad log line
- Hello I am a bad log line"""
    )
