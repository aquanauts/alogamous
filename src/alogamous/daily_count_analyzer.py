import datetime

from alogamous import analyzer, log_line_parser


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
        all_report_messages = []
        all_report_messages.extend(self.format_report(self.info_counts, "info"))
        all_report_messages.extend(self.format_report(self.warning_counts, "warning"))
        all_report_messages.extend(self.format_report(self.error_counts, "error"))
        if all_report_messages:
            out_stream.write("\n".join(all_report_messages))
        else:
            out_stream.write("There has been no daily increase in specific types of messages for any service")

    @staticmethod
    def format_report(dictionary, level):
        report_messages = []
        for service in dictionary:
            difference_messages = []
            sorted_days = sorted(dictionary[service])
            for previous_day_index, day in enumerate(sorted_days[1:]):
                previous_day = sorted_days[previous_day_index]
                difference = dictionary[service][day] - dictionary[service][previous_day]
                if difference > 0:
                    difference_messages.append(
                        f"- On {day}, the number of {level} messages increased by {difference} from the previous day"
                    )
            if difference_messages:
                report_messages.append(f"Daily increases in {level} log message for {service}:")
                report_messages.extend(difference_messages)
        return report_messages
