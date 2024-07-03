import io

from alogamous import analyzer, error_counter_analyzer


def test_error_counter():
    in_stream = io.StringIO("""line1
        blahblahERRORblah
        oh_no_another_ERROR""")
    out_stream = io.StringIO()
    analyzer.analyze_log_stream([error_counter_analyzer.ErrorCounterAnalyzer()], in_stream, out_stream)
    assert out_stream.getvalue().strip() == "There are 2 error lines in this log"
