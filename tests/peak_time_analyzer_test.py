import io

from alogamous import analyzer, peak_time_analyzer


def test_no_errors():
    in_stream = io.StringIO(
        """2024-06-20 11:00:17,983 - root - INFO - Adding subscription for pid None
2024-06-20 11:00:18,115 - root - INFO - Initialized Influx DB Client to host
2024-06-20 11:00:18,115 - root - INFO - Scheduling Error Handler in 150.0 seconds
2024-06-20 11:00:18,116 - root - INFO - prometheus client http server running
2024-06-20 11:00:18,172 - root - INFO - Initialized prometheus server.
2024-06-20 11:00:18,172 - root - INFO - reading messages from 2024-06-20
2024-06-20 11:00:18,172 - aiokafka.consumer.subscription_state - INFO - Updating subscribed topics to: frozenset({'internal'})
2024-06-20 11:00:18,185 - root - INFO - Kafka reading from start of day 2024-06-20 05:00:00+00:00 on topic internal from kafka.servers:9092
2024-06-20 11:00:19,328 - root - INFO - Kafka source starting for topic internal at current offset 7924032 end offset 7928950 on servers kafka.servers:9092
2024-06-20 11:00:22,329 - root - INFO - Kafka topic internal is caught up at offset 7928949
2024-06-20 11:00:22,329 - root - INFO - setting influx write rate to pre-market hours frequency
2024-06-20 11:00:22,329 - root - INFO - Tracking service is caught up
2024-06-20 11:40:43,527 - root - WARNING - instrument not found for sedol BYP321337
2024-06-20 11:40:43,527 - root - WARNING - Could not find instrument for sedol BYP321337, trying ric YT.ATS
2024-06-20 11:40:43,527 - root - WARNING - instrument not found for ric YT.ATS
2024-06-20 11:40:43,527 - root - WARNING - Could not find instrument for ric YT.ATS, using provided identifier 1
2024-06-20 11:40:43,527 - root - WARNING - instrument not found for sedol DHI7337
2024-06-20 11:40:43,527 - root - WARNING - Could not find instrument for sedol DHI7337, trying ric YT.ATS
2024-06-20 11:40:43,529 - root - WARNING - instrument not found for ric JPQ.CC
2024-06-20 11:40:43,529 - root - WARNING - Could not find instrument for ric JPQ.CC, using provided identifier 2
2024-06-20 11:40:43,529 - root - WARNING - instrument not found for sedol RZZZZ2
2024-06-20 11:40:43,529 - root - WARNING - Could not find instrument for sedol RZZZZ2, trying ric UYU.T
2024-06-20 11:40:43,529 - root - WARNING - instrument not found for ric UYU.T
2024-06-20 11:40:43,529 - root - WARNING - Could not find instrument for ric UTU.T, using provided identifier 3
2024-06-20 11:40:43,529 - root - WARNING - instrument not found for sedol OIN38378
2024-06-20 11:40:43,529 - root - WARNING - Could not find instrument for sedol OIN38378, trying ric 837.RIJ
2024-06-20 11:40:43,529 - root - WARNING - instrument not found for ric 837.RIJ
2024-06-20 11:40:43,529 - root - WARNING - Could not find instrument for ric 837.RIJ, using provided identifier 4
2024-06-20 11:40:43,529 - root - WARNING - instrument not found for sedol UY29387
2024-06-20 11:40:43,529 - root - WARNING - Could not find instrument for sedol UY29387, trying ric RUE.ST
2024-06-20 11:40:43,529 - root - WARNING - instrument not found for ric RUE.ST
2024-06-20 11:40:43,529 - root - WARNING - Could not find instrument for ric RUE.ST, using provided identifier 5
2024-06-20 17:16:03,660 - root - ERROR - Caught exception N/A. Message: Unclosed client session NoneType: None
2024-06-20 17:16:03,660 - root - ERROR - Caught exception N/A. Message: Unclosed connector NoneType: None
2024-06-20 17:17:04,278 - root - INFO - Updating prices
2024-06-20 17:24:34,091 - root - INFO - Closing client connection.
2024-06-20 17:24:34,092 - root - INFO - Client (0)ui-tracking_service Closed
2024-06-20 17:25:08,029 - root - ERROR - Exception in message handler <bound method TrackingService.method of <app.tracking_service."""
    )
    out_stream = io.StringIO()
    analyzer.analyze_log_stream([peak_time_analyzer.PeakTimeAnalyzer()], in_stream, out_stream)
    assert (
        out_stream.getvalue()
        == "there are 7 peak time ranges: ['2024-06-20 11:00:18.115000 - 2024-06-20 11:00:18.116000', '2024-06-20 11:00:18.172000 - 2024-06-20 11:00:18.172000', '2024-06-20 11:00:22.329000 - 2024-06-20 11:00:22.329000', '2024-06-20 11:40:43.527000 - 2024-06-20 11:40:43.527000', '2024-06-20 11:40:43.529000 - 2024-06-20 11:40:43.529000', '2024-06-20 17:16:03.660000 - 2024-06-20 17:16:03.660000', '2024-06-20 17:24:34.091000 - 2024-06-20 17:24:34.092000']\n"
        "\n"
        "------ a report has been reported ------\n"
        "\n"
    )


def test_faulty_lines():
    in_stream = io.StringIO("""this is a faulty log line
====================================================
STARTING Tracking service
Start time: 2024-06-21 09:00:00.001550+00:00
Version: 2729a
Command line: ['.venv/bin/python3', '-m', 'app.tracking_service', '--market', 'US', '--version', '2729a']
2024-06-20 11:555:0001,1234 - root - INFO - messages
""")
    out_stream = io.StringIO()
    analyzer.analyze_log_stream([peak_time_analyzer.PeakTimeAnalyzer()], in_stream, out_stream)
    assert (
        out_stream.getvalue().strip() == "there are 0 peak time ranges: []\n\n------ a report has been reported ------"
    )


def test_one_line():
    in_stream = io.StringIO("2024-06-20 11:40:01,000 - root - WARNING - Could not find instrument for sedol UY29387")
    out_stream = io.StringIO()
    analyzer.analyze_log_stream([peak_time_analyzer.PeakTimeAnalyzer()], in_stream, out_stream)
    assert (
        out_stream.getvalue().strip() == "there are 0 peak time ranges: []\n\n------ a report has been reported ------"
    )


def test_no_lines():
    in_stream = io.StringIO("")
    out_stream = io.StringIO()
    analyzer.analyze_log_stream([peak_time_analyzer.PeakTimeAnalyzer()], in_stream, out_stream)
    assert (
        out_stream.getvalue().strip() == "there are 0 peak time ranges: []\n\n------ a report has been reported ------"
    )
