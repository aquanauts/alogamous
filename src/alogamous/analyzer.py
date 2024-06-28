import sys
from abc import ABC


class Analyzer(ABC):
    def read_log_line(self, line):
        pass

    def report(self, out_stream):
        pass


def analyze_log_stream(analyzers, in_stream, out_stream):
    for line in in_stream:
        for analyzer in analyzers:
            analyzer.read_log_line(line.rstrip())
    for analyzer in analyzers:
        analyzer.report(out_stream)


if __name__ == "__main__":
    analyze_log_stream(sys.stdin, sys.stdout)

