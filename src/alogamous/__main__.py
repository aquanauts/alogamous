from alogamous import (
    analyzer,
    directory_reader,
    echo_analyzer,
    error_counter_analyzer,
    line_count_analyzer,
    loginfo_analyzer,
    warning_analyzer,
)

with open("../../data/test_output_file.txt", "a") as output_file:
    reader = directory_reader.DirectoryReader("../../data")
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
