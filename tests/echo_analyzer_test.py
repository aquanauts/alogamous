import io

from alogamous.echo_analyzer import EchoAnalyzer


def test_echo_lines():
    line_echoer = EchoAnalyzer()
    in_stream = """line1
        line2
        line3"""
    out_stream = io.StringIO()

    line_echoer.read_log_line(in_stream)
    line_echoer.report(out_stream)
    assert (
        out_stream.getvalue()
        == """line1
        line2
        line3"""
    )


def test_echo_no_lines():
    line_echoer = EchoAnalyzer()
    out_stream = io.StringIO()
    line_echoer.report(out_stream)
    assert out_stream.getvalue() == ""
