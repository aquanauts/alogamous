import sys

from alogamous import analyzer, echo_analyzer, error_counter_analyzer, line_count_analyzer

analyzer.analyze_log_stream(
    [
        echo_analyzer.EchoAnalyzer(),
        error_counter_analyzer.ErrorCounterAnalyzer(),
        line_count_analyzer.LineCountAnalyzer(),
    ],
    sys.stdin,
    sys.stdout,
)
