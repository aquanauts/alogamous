import io

from alogamous import analyzer, echo_analyzer


def test_echo_lines():
    in_stream = io.StringIO("""line1
        line2
        line3""")
    out_stream = io.StringIO()
    analyzer.analyze_log_stream([echo_analyzer.EchoAnalyzer()], in_stream, out_stream)
    assert (
        out_stream.getvalue()
        == """line1
        line2
        line3"""
    )
