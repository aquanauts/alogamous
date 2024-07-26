import sys

from alogamous import (
    analyzer,
    directory_reader,
    error_counter_analyzer,
    flag_duplicate_log_messages,
    line_count_analyzer,
    log_line_parser,
    loginfo_analyzer,
    startup_header_analyzer,
    warning_analyzer,
)

expected_arg_len = 4

if len(sys.argv) != expected_arg_len:
    sys.stdout.write(f"Usage: {sys.argv[0]} <LOG_CONFIG> <INPUT_DIRECTORY> <OUTPUT_FILE>")
    sys.stdout.write("\nPossible LOG_CONFIGS are:")
    for key in log_line_parser.LOG_FILE_CONFIGS:
        sys.stdout.write(f"\n- {key}")
    sys.stdout.write("\nINPUT_DIRECTORY must be file path to a directory of log files")
    sys.stdout.write("\nOUTPUT_FILE must be file path to the file you want the log report written in")
    sys.exit(1)

with open(f"{sys.argv[3]}", "a") as output_file:
    reader = directory_reader.DirectoryReader(f"{sys.argv[2]}")
    expected_fields = list(
        log_line_parser.LOG_FILE_CONFIGS[sys.argv[1]][log_line_parser.ConfigParameters.EXPECTED_FIELDS]
    )
    seperator = str(log_line_parser.LOG_FILE_CONFIGS[sys.argv[1]][log_line_parser.ConfigParameters.SEPERATOR])
    header_line = str(log_line_parser.LOG_FILE_CONFIGS[sys.argv[1]][log_line_parser.ConfigParameters.HEADER_LINE])
    line_parser = log_line_parser.LogLineParser(expected_fields, seperator, header_line)
    analyzer.analyze_log_stream(
        [
            # echo_analyzer.EchoAnalyzer(),
            error_counter_analyzer.ErrorCounterAnalyzer(),
            flag_duplicate_log_messages.FlagDuplicateLogMessages(),
            line_count_analyzer.LineCountAnalyzer(),
            loginfo_analyzer.InfoAnalyzer(line_parser),
            startup_header_analyzer.StartupHeaderAnalyzer(line_parser),
            warning_analyzer.WarningAnalyzer(),
        ],
        reader.read(),
        output_file,
    )
