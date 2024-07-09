import datetime


class LogLineUtility:

    @staticmethod
    def tokenize(text, splitter):
        return text.split(splitter)

    @staticmethod
    def parse_date(text, dt_format):
        return datetime.datetime.strptime(text, dt_format)


