from io import StringIO

from alogamous import log_line_parser, stack_trace_analyzer


def test_stacktrace_where_service_dies():
    parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    stacktrace_checker = stack_trace_analyzer.StackTraceAnalyzer(parser)
    in_stream = """2024-07-23 21:13:53,862 - root - INFO - Closing client connection.
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
AttributeError: 'NoneType' object has no attribute 'region'"""
    out_stream = StringIO()
    for line in in_stream.splitlines():
        stacktrace_checker.read_log_line(line)
    stacktrace_checker.report(out_stream)
    assert out_stream.getvalue() == "No non-fatal stack traces were found"


def test_stacktrace_where_service_lives():
    parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    stacktrace_checker = stack_trace_analyzer.StackTraceAnalyzer(parser)
    in_stream = """2024-07-23 21:13:53,862 - root - INFO - Closing client connection.
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
2024-07-23 21:13:54,091 - root - ERROR - Caught exception N/A. Message: Unclosed client session"""
    out_stream = StringIO()
    for line in in_stream.splitlines():
        stacktrace_checker.read_log_line(line)
    stacktrace_checker.report(out_stream)
    assert (
        out_stream.getvalue()
        == """1 non-fatal stack trace(s) found:
- Traceback (most recent call last):
-   File "<frozen runpy>", line 1938, in _run_module_as_main
-   File "<frozen runpy>", line 88, in _run_code
-   File ".build/2811/execution/execution_service", line 973, in <module>
-     app.run(life_cycle_runner.run, life_cycle_runner.stop)
-   File ".build/2811/app/application.py", line 219, in run
-     run(self.start(my_date, main, stop))
-   File ".build/2811/.venv/lib/python3.11/runners.py", line 190, in run
-     return runner.run(main)
-            ^^^^^^^^^^^^^^^^
-   File ".build/2811/.venv/lib/python3.11/runners.py", line 118, in run
-     return self._loop.run_until_complete(task)
-            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-   File ".build/2811/.venv/lib/python3.11/events.py", line 653, in run_until_done
-     return future.result()
-            ^^^^^^^^^^^^^^^
-   File "2811/app/application.py", line 421, in start
-     await self.task
-   File "2811/messages/app/runner.py", line 449, in run
-     await asyncio.gather(*self.running_tasks)
-   File "2811/messages/processor.py", line 340, in run
-     await self.dispatch(message)
-   File ".build/2811/execution/execution_service", line 1315, in market_test
-     if symbol and obj.region != 'NORTHAMERICA'
-                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- AttributeError: 'NoneType' object has no attribute 'region'"""
    )


def test_no_stacktrace():
    parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    stacktrace_checker = stack_trace_analyzer.StackTraceAnalyzer(parser)
    in_stream = """2024-07-23 21:13:53,862 - root - INFO - Closing client connection.
    2024-07-23 21:13:53,862 - root - INFO - Closing client connection."""
    out_stream = StringIO()
    for line in in_stream.splitlines():
        stacktrace_checker.read_log_line(line)
    stacktrace_checker.report(out_stream)
    assert out_stream.getvalue() == "No non-fatal stack traces were found"
