from abc import ABC, abstractmethod


class Analyzer(ABC):
    @abstractmethod
    def read_log_line(self, line):
        pass

    @abstractmethod
    def report(self, out_stream):
        pass


def analyze_log_stream(analyzers, in_stream, out_stream):
    for line in in_stream:
        for analyzer in analyzers:
            analyzer.read_log_line(line.rstrip())
    for analyzer in analyzers:
        analyzer.report(out_stream)
        # out_stream.write("\n>>>>>>>>>> a report has been reported <<<<<<<<<<\n")
