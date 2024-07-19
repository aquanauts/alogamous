import sys

from alogamous import analyzer, echo_analyzer, line_count_analyzer, loginfo_analyzer

analyzer.analyze_log_stream(
    [echo_analyzer.EchoAnalyzer(), line_count_analyzer.LineCountAnalyzer(), loginfo_analyzer.InfoAnalyzer()],
    sys.stdin,
    sys.stdout,
)
