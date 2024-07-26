from __future__ import annotations


class ConfigParameters:
    EXPECTED_FIELDS = "expected fields"
    SEPERATOR = "seperator"
    HEADER_LINE = "header line"


LOG_FILE_CONFIGS = {
    "default": {
        ConfigParameters.EXPECTED_FIELDS: ["datetime", "source", "level", "message"],
        ConfigParameters.SEPERATOR: " - ",
        ConfigParameters.HEADER_LINE: "====================================================",
    }
}


class LineType:
    HEADER_LINE = "header line"
    LOG_LINE = "log line"
    UNSTRUCTURED_LINE = "unstructured line"


class LogLineParser:
    def __init__(self, expected_fields: list[str], seperator: str, header_line: str):
        self.header_line = header_line
        self.expected_fields = expected_fields
        self.separator = seperator
        self.separator_count = len(self.expected_fields) - 1

    def parse(self, line):
        if line == self.header_line:
            return {"type": LineType.HEADER_LINE, "line": line}
        if line.count(self.separator) == self.separator_count:
            parsed_line = {"type": LineType.LOG_LINE}
            separated_line = line.split(self.separator)
            for index in range(len(self.expected_fields)):
                parsed_line[self.expected_fields[index]] = separated_line[index]
            return parsed_line
        return {"type": LineType.UNSTRUCTURED_LINE, "line": line}
