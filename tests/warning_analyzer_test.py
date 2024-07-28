import io

from alogamous import warning_analyzer


def test_warning_count():
    counter = warning_analyzer.WarningAnalyzer()
    in_stream = io.StringIO("""2024-06-20 11:00:18,185 - root - INFO - Kafka reading from start of day 2024-06-20 05:00:00+00:00 on topic internal from kafka.servers:9092
2024-06-20 11:00:19,328 - root - INFO - Kafka source starting for topic internal at current offset 7924032 end offset 7928950 on servers kafka.servers:9092
2024-06-20 11:00:22,329 - root - INFO - Kafka topic internal is caught up at offset 7928949
2024-06-20 11:00:22,329 - root - INFO - setting influx write rate to pre-market hours frequency
2024-06-20 11:00:22,329 - root - INFO - Tracking service is caught up
2024-06-20 11:40:43,527 - root - WARNING - instrument not found for sedol BYP321337
2024-06-20 11:40:43,527 - root - WARNING - instrument not found for sedol BYP321337
2024-06-20 17:25:08,029 - root - ERROR - Exception in message handler <bound method TrackingService.method of <app.tracking_service.TrackingService object at 0x7feba0d0>> TrackingService.on_order_change() missing 1 required positional argument: 'order_identifier'""")
    out_stream = io.StringIO()
    for line in in_stream:
        counter.read_log_line(line)
    counter.report(out_stream)
    assert out_stream.getvalue() == "\n2 Warnings were detected."
