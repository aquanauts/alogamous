import sys

from alogamous import analyzer, echo_analyzer

analyzer.analyze_log_stream([echo_analyzer.EchoAnalyzer()], sys.stdin, sys.stdout)
