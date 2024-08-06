import statistics
from abc import ABC
from datetime import datetime

from alogamous import analyzer


class PeakTimeAnalyzer(analyzer.Analyzer, ABC):
    def __init__(self):
        self.d = {}
        self.peaktimes = []
        self.timestamps = []
        self.sort_by_val = []
        self.ranges = []
        self.lines_to_delete = []

    def read_log_line(self, line):
        timestamp = line.split(" - ")[0]
        try:
            timestamp = datetime.fromisoformat(timestamp)
            self.timestamps.append(timestamp)
        except ValueError:
            del timestamp

    def report(self, out_stream):
        for i in range(len(self.timestamps) - 1):
            value = (self.timestamps[i + 1] - self.timestamps[i]).total_seconds()
            timerange = f"{self.timestamps[i]} - {self.timestamps[i+1]}"
            self.d[timerange] = value
        values = list(self.d.values())
        minimum = 2
        if len(self.d) >= minimum:
            mean = statistics.mean(values)
            for timerange in self.d:
                self.sort_by_val.append(f"{self.d[timerange]} = {timerange}")
                for line in self.sort_by_val:
                    if float(line.split(" = ")[0]) >= mean:
                        self.sort_by_val.remove(line)
            self.sort_by_val.sort()
            half = len(self.sort_by_val) // 2
            lower_half = self.sort_by_val[:half]
            for line in lower_half:
                v, t = line.split(" = ")
                self.ranges.append(t)
            self.ranges.sort()

            for index in range(len(self.ranges) - 1):
                start_a, stop_a = self.ranges[index].split(" - ")
                start_b, stop_b = self.ranges[index + 1].split(" - ")
                if stop_a == start_b:
                    self.ranges[index] = f"{start_a} - {stop_b}"
                    self.lines_to_delete.append(self.ranges[index + 1])

            for line in self.ranges:
                if line in self.lines_to_delete:
                    self.ranges.remove(line)

        else:
            self.ranges = []

        out_stream.write(f"there are {len(self.ranges)} peak time ranges: {self.ranges}")
