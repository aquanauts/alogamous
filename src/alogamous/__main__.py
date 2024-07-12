from alogamous import analyzer, echo_analyzer, line_count_analyzer

with open("../../data/ex_log_01.txt") as log_file, open("../../data/test_output_file.txt", "a") as output_file:
    analyzer.analyze_log_stream(
        [echo_analyzer.EchoAnalyzer(), line_count_analyzer.LineCountAnalyzer()], log_file, output_file
    )
