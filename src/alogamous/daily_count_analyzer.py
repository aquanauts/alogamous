import datetime

from alogamous import analyzer, log_line_parser


class DailyCountAnalyzer(analyzer.Analyzer):
    def __init__(self, line_parser):
        self.parser = line_parser
        self.header_line_count = 0
        self.current_service = ""
        self.info_counts_by_service_by_day = {}
        self.warning_counts_by_service_by_day = {}
        self.error_counts_by_service_by_day = {}

    def read_log_line(self, line):
        parsed_line = self.parser.parse(line)
        self._find_service_line(line, parsed_line)
        if parsed_line["type"] == log_line_parser.LineType.LOG_LINE:
            date_object = self._create_date_object(parsed_line)
            line_level = parsed_line["level"].lower()
            if line_level == "info":
                self._update_dictionary_count(self.info_counts_by_service_by_day, self.current_service, date_object)
            elif line_level.count("warn") == 1:
                self._update_dictionary_count(self.warning_counts_by_service_by_day, self.current_service, date_object)
            elif line_level == "error":
                self._update_dictionary_count(self.error_counts_by_service_by_day, self.current_service, date_object)

    def report(self, out_stream):
        all_report_messages = []
        all_report_messages.extend(self._format_report(self.info_counts_by_service_by_day, "info"))
        all_report_messages.extend(self._format_report(self.warning_counts_by_service_by_day, "warning"))
        all_report_messages.extend(self._format_report(self.error_counts_by_service_by_day, "error"))
        if all_report_messages:
            out_stream.write("\n".join(all_report_messages))
        else:
            out_stream.write("There has been no daily increase in specific types of messages for any service")

    def _find_service_line(self, line, parsed_line):
        if parsed_line["type"] == log_line_parser.LineType.HEADER_LINE:
            self.header_line_count += 1
        elif self.header_line_count % 2 == 1 and line.count("STARTING") == 1:
            self.current_service = line.replace("STARTING ", "")

    @staticmethod
    def _create_date_object(parsed_line):
        if parsed_line["datetime"].count(" ") == 1:
            date_string = parsed_line["datetime"].split(" ")[0]
        else:
            date_string = parsed_line["datetime"].split("T")[0]
        return datetime.datetime.strptime(date_string, "%Y-%m-%d").astimezone(datetime.timezone.utc).date()

    @staticmethod
    def _update_dictionary_count(counts_by_service_by_day, service, date):
        if counts_by_service_by_day.get(service) is None:
            counts_by_service_by_day[service] = {date: 1}
        elif counts_by_service_by_day[service].get(date) is None:
            counts_by_service_by_day[service][date] = 1
        else:
            counts_by_service_by_day[service][date] += 1

    @staticmethod
    def _format_report(counts_by_service_by_day, level):
        report_messages = []
        for service in counts_by_service_by_day:
            difference_messages = []
            sorted_days = sorted(counts_by_service_by_day[service])
            for previous_day_index, day in enumerate(sorted_days[1:]):
                previous_day = sorted_days[previous_day_index]
                difference = counts_by_service_by_day[service][day] - counts_by_service_by_day[service][previous_day]
                if difference > 0:
                    difference_messages.append(
                        f"- On {day}, the number of {level} messages increased by {difference} from the previous day"
                    )
            if difference_messages:
                report_messages.append(f"Daily increases in {level} log message for {service}:")
                report_messages.extend(difference_messages)
        return report_messages
