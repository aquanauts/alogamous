import io

from alogamous.log_line_parser import LogLineParser
from alogamous.loginfo_analyzer import InfoAnalyzer


def test_report():
    infomessage_counter = InfoAnalyzer(LogLineParser(["log_level", "message"], ":", "HEADER"))
    out_stream = io.StringIO()

    infomessage_counter.read_log_line("HEADER")
    infomessage_counter.read_log_line("info: line 1")
    infomessage_counter.read_log_line("info: line 2")
    infomessage_counter.read_log_line("info: line 3")
    infomessage_counter.read_log_line("info: line 4")
    infomessage_counter.read_log_line("warning: this line has information")
    infomessage_counter.report(out_stream)

    assert out_stream.getvalue().strip() == "Number of info messages: 4"


def test_capital_info():
    infomessage_counter = InfoAnalyzer(LogLineParser(["log_level", "message"], ":", "HEADER"))
    out_stream = io.StringIO()

    infomessage_counter.read_log_line("Info: line 1")
    infomessage_counter.read_log_line("warning: line 2")
    infomessage_counter.read_log_line("info: line 3")
    infomessage_counter.read_log_line("error: line 4")
    infomessage_counter.report(out_stream)

    assert out_stream.getvalue().strip() == "Number of info messages: 2"


def test_report_mixedlines():
    infomessage_counter = InfoAnalyzer(LogLineParser(["log_level", "message"], ":", "HEADER"))
    out_stream = io.StringIO()

    infomessage_counter.read_log_line("info: line 1")
    infomessage_counter.read_log_line("warning: line 2")
    infomessage_counter.read_log_line("info: line 3")
    infomessage_counter.read_log_line("error: line 4")
    infomessage_counter.report(out_stream)

    assert out_stream.getvalue().strip() == "Number of info messages: 2"


def test_report_without_info_messages():
    infomessage_counter = InfoAnalyzer(LogLineParser(["log_level", "message"], ":", "HEADER"))
    out_stream = io.StringIO()

    infomessage_counter.read_log_line("Warning: line 1")
    infomessage_counter.read_log_line("Error: line 2")
    infomessage_counter.read_log_line("Error: line 3")

    infomessage_counter.report(out_stream)

    assert out_stream.getvalue().strip() == "Number of info messages: 0"


def test_no_imput_lines():
    infomessage_counter = InfoAnalyzer(LogLineParser(["log_level", "message"], ":", "HEADER"))
    out_stream = io.StringIO()

    infomessage_counter.report(out_stream)

    assert out_stream.getvalue().strip() == "Number of info messages: 0"
