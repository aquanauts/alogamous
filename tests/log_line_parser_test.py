from alogamous import log_line_parser


def test_parse_header_line():
    parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    line = "===================================================="
    assert parser.parse(line) == {"type": "header line", "line": "===================================================="}


def test_parse_log_line():
    parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    line = (
        "2024-06-20 11:00:18,172 - aiokafka.consumer.subscription_state - INFO - Updating subscribed topics to: "
        "frozenset({'internal'})"
    )
    assert parser.parse(line) == {
        "type": "log line",
        "datetime": "2024-06-20 11:00:18,172",
        "source": "aiokafka.consumer.subscription_state",
        "level": "INFO",
        "message": "Updating subscribed topics to: frozenset({'internal'})",
    }


def test_parse_deviant_log_line():
    parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    line = "Hello I am a bad log line"
    assert parser.parse(line) == {"type": "unstructured line", "line": "Hello I am a bad log line"}


def test_parse_start_header_content():
    parser = log_line_parser.LogLineParser(
        ["datetime", "source", "level", "message"], " - ", "===================================================="
    )
    line = "    Start time: 2024-06-20 09:00:00.001550+00:00"
    assert parser.parse(line) == {
        "type": "unstructured line",
        "line": "    Start time: 2024-06-20 09:00:00.001550+00:00",
    }


def test_parse_complex_log_line():
    parser = log_line_parser.LogLineParser(
        [["datetime", "thread", "level", "source"], ["message"]],
        " - ",
        "====================================================",
        " ",
    )
    line = "2024-06-28T12:00:00.460+0000 [main] INFO com.app.java_process.info - Starting with config"
    assert parser.parse(line) == {
        "type": "log line",
        "datetime": "2024-06-28T12:00:00.460+0000",
        "thread": "[main]",
        "level": "INFO",
        "source": "com.app.java_process.info",
        "message": "Starting with config",
    }
