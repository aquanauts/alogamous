from __future__ import annotations


class ConfigParameters:
    EXPECTED_FIELDS = "expected fields"
    SEPERATOR = "separator"
    HEADER_LINE = "header line"
    SEPARATOR2 = "separator2"


LOG_FILE_CONFIGS = {
    "python_logs": {
        ConfigParameters.EXPECTED_FIELDS: ["datetime", "source", "level", "message"],
        ConfigParameters.SEPERATOR: " - ",
        ConfigParameters.HEADER_LINE: "====================================================",
    },
    "java_logs": {
        ConfigParameters.EXPECTED_FIELDS: [["datetime", "thread", "level", "source"], ["message"]],
        ConfigParameters.SEPERATOR: " - ",
        ConfigParameters.HEADER_LINE: "====================================================",
        ConfigParameters.SEPARATOR2: " ",
    },
}


class LineType:
    HEADER_LINE = "header line"
    LOG_LINE = "log line"
    UNSTRUCTURED_LINE = "unstructured line"


class LogLineParser:
    def __init__(self, expected_fields: list, seperator: str, header_line: str, separator2=None):
        self.header_line = header_line
        self.expected_fields = expected_fields
        self.separator = seperator
        self.separator2 = separator2
        self.separator_count = len(self.expected_fields) - 1
        self.separator2_count = len(self.expected_fields[0]) - 1

    def parse(self, line):
        if line == self.header_line:
            return {"type": LineType.HEADER_LINE, "line": line}
        if line.count(self.separator) == self.separator_count:
            if self.separator2 is None:
                return self.parse_simple_line(line)
            return self.parse_complex_line(line)
        return {"type": LineType.UNSTRUCTURED_LINE, "line": line}

    def parse_simple_line(self, line):
        parsed_line = {"type": LineType.LOG_LINE}
        separated_line = line.split(self.separator)
        for index in range(len(self.expected_fields)):
            parsed_line[self.expected_fields[index]] = separated_line[index]
        return parsed_line

    def parse_complex_line(self, line):
        parsed_line = {"type": LineType.LOG_LINE}
        chunked_line = line.split(self.separator)
        separated_line = chunked_line[0].split(self.separator2)
        separated_line.append(chunked_line[1])
        index = 0
        for field_list in self.expected_fields:
            for field in field_list:
                parsed_line[field] = separated_line[index]
                index += 1
        return parsed_line
