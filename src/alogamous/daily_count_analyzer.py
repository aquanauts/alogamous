import datetime

from alogamous import analyzer, log_line_parser


# supposed to track and compare for only one service
# currently assumes all lines are from one service, may need to change in future
# current plan to fix this is to have "internal" and "external" report methods
# the "internal" report would save information so that the real report can it access later
# so when a header line is detected, it can internally report results and clear variables and start over
# and then when the real report is called, it can access the internally reported info for the final report
class DailyCountAnalyzer(analyzer.Analyzer):
    def __init__(self, line_parser):
        self.parser = line_parser
        self.header_line_count = 0
        self.current_service = ""
        self.info_counts = {}
        self.warning_counts = {}
        self.error_counts = {}

    def read_log_line(self, line):
        parsed_line = self.parser.parse(line)
        if parsed_line["type"] == log_line_parser.LineType.HEADER_LINE:
            self.header_line_count += 1
        elif self.header_line_count % 2 == 1 and line.count("STARTING") == 1:
            self.current_service = line.replace("STARTING ", "")
        elif parsed_line["type"] == log_line_parser.LineType.LOG_LINE:
            if parsed_line["datetime"].count(" ") == 1:
                date_string = parsed_line["datetime"].split(" ")[0]
            else:
                date_string = parsed_line["datetime"].split("T")[0]
            date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d").astimezone(datetime.timezone.utc).date()
            line_level = parsed_line["level"].lower()
            if line_level == "info":
                self.update_dictionary_count(self.info_counts, self.current_service, date_object)
            elif line_level.count("warn") == 1:
                self.update_dictionary_count(self.warning_counts, self.current_service, date_object)
            elif line_level == "error":
                self.update_dictionary_count(self.error_counts, self.current_service, date_object)

    @staticmethod
    def update_dictionary_count(dictionary, service, date):
        if dictionary.get(service) is None:
            dictionary[service] = {date: 1}
        elif dictionary[service].get(date) is None:
            dictionary[service][date] = 1
        else:
            dictionary[service][date] += 1

    def report(self, out_stream):
        self.report_increases(self.info_counts, "info", out_stream)
        self.report_increases(self.warning_counts, "warning", out_stream)
        self.report_increases(self.error_counts, "error", out_stream)

    @staticmethod
    def report_increases(dictionary, level, out_stream):
        for service in dictionary:
            out_stream.write(f"Daily increases in types of log message for {service}:")
            sorted_days = sorted(dictionary[service])
            for previous_day_index, day in enumerate(sorted_days[1:]):
                previous_day = sorted_days[previous_day_index]
                difference = dictionary[service][day] - dictionary[service][previous_day]
                if difference > 0:
                    out_stream.write(
                        f"\n- On {day}, the number of {level} messages increased by {difference} from previous day"
                    )
