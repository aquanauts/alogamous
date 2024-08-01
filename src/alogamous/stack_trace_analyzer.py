from alogamous import analyzer, log_line_parser


class StackTraceAnalyzer(analyzer.Analyzer):
    def __init__(self, line_parser):
        self.parser = line_parser
        self.stack_trace = False
        self.stack_trace_counter = 0
        self.stack_trace_lines = []
        self.non_fatal_trace = False

    def read_log_line(self, line):
        line_type = self.parser.parse(line)["type"]
        if line_type == log_line_parser.LineType.UNSTRUCTURED_LINE and line.count("Traceback") == 1:
            self.stack_trace = True
            self.stack_trace_counter += 1
            self.stack_trace_lines.append(line)
        elif self.stack_trace:
            if line_type == log_line_parser.LineType.UNSTRUCTURED_LINE:
                self.stack_trace_lines.append(line)
            elif line_type == log_line_parser.LineType.HEADER_LINE:
                self.stack_trace = False
            elif line_type == log_line_parser.LineType.LOG_LINE:
                self.stack_trace = False
                self.non_fatal_trace = True

    def report(self, out_stream):
        if self.non_fatal_trace:
            out_stream.write(f"{self.stack_trace_counter} non-fatal stack trace(s) found:\n- ")
            out_stream.write("\n- ".join(self.stack_trace_lines))
        else:
            out_stream.write("No non-fatal stack traces were found")
