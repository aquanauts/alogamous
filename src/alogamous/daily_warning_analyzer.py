import datetime

from alogamous import analyzer, log_line_parser


class DailyWarningAnalyzer(analyzer.Analyzer):
    def __init__(self, parser):
        self.warningMessages: dict[str, list[datetime]] = {}
        self.dailyWarningMessages: dict[str, list[datetime]] = {}
        self.parser = parser

    def read_log_line(self, line):
        parsed_line = self.parser.parse(line)
        line_type = parsed_line["type"]
        if line_type == log_line_parser.LineType.LOG_LINE and parsed_line["level"].lower() == "warning":
            message = parsed_line["message"]
            date_string = parsed_line["datetime"]
            date = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S,%f").astimezone(datetime.timezone.utc)
            if message not in self.warningMessages:
                self.warningMessages[message] = [date]
            else:
                last_warning_date = self.warningMessages[message][-1]
                if (date - last_warning_date).days == 1:
                    if message not in self.dailyWarningMessages:
                        self.dailyWarningMessages[message] = [last_warning_date]
                    self.warningMessages[message].append(date)
                    self.dailyWarningMessages[message].append(date)

    def report(self, out_stream):
        if len(self.dailyWarningMessages) > 0:
            out_stream.write("Daily warning messages:\n")
            for message in self.dailyWarningMessages:
                out_stream.write(f"{message}\n")
        else:
            out_stream.write("There are no daily warning messages.\n")
