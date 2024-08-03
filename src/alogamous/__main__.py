from alogamous import (
    analyzer,
    directory_reader,
    echo_analyzer,
    error_counter_analyzer,
    line_count_analyzer,
    peak_time_analyzer,
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
            peak_time_analyzer.PeakTimeAnalyzer(),
        ],
        reader.read(),
        output_file,
    )
