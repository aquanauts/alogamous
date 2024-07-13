from __future__ import annotations


class LogLineParser:
    def __init__(self, header_line: str, expected_fields: list[str], seperator: str):
        self.header_line = header_line
        self.expected_fields = expected_fields
        self.separator = seperator
        self.separator_count = len(self.expected_fields) - 1

    def parse(self, line):
        if line == self.header_line:
            return {"type": "header line", "line": line}
        if line.count(self.separator) == self.separator_count:
            parsed_line = {"type": "log line"}
            separated_line = line.split(self.separator)
            for index in range(len(self.expected_fields)):
                parsed_line[self.expected_fields[index]] = separated_line[index]
            return parsed_line
        return {"type": "unstructured line", "line": line}
