import sys

from alogamous import analyzer, echo_analyzer, line_count_analyzer

analyzer.analyze_log_stream(
    [echo_analyzer.EchoAnalyzer(), line_count_analyzer.LineCountAnalyzer()], sys.stdin, sys.stdout
)
