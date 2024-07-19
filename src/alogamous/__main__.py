import sys

from alogamous import (
    analyzer,
    directory_reader,
    echo_analyzer,
    error_counter_analyzer,
    line_count_analyzer,
    log_line_parser,
    loginfo_analyzer,
    warning_analyzer,
)

if len(sys.argv) != int(sys.argv[1]) + 4:
    sys.stdout.write(f"Usage: {sys.argv[0]} <NUM_FIELDS> <FIELD_NAME1> <FIELD_NAME2> ... <SEPARATOR> <HEADER_LINE>")
    sys.exit(1)

expected_fields = sys.argv[2 : int(sys.argv[1]) + 2]

with open("../../data/test_output_file.txt", "a") as output_file:
    reader = directory_reader.DirectoryReader("../../data")
    line_parser = log_line_parser.LogLineParser(
        expected_fields, sys.argv[int(sys.argv[1]) + 2], sys.argv[int(sys.argv[1]) + 3]
    )
    analyzer.analyze_log_stream(
        [
            echo_analyzer.EchoAnalyzer(),
            error_counter_analyzer.ErrorCounterAnalyzer(),
            line_count_analyzer.LineCountAnalyzer(),
            warning_analyzer.WarningAnalyzer(),
            loginfo_analyzer.InfoAnalyzer(),
        ],
        reader.read(),
        output_file,
    )
