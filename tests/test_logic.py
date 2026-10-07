import io
import json
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace

import controller_bai3 as controller
import device_bai3 as device
import monitor_subscriber_bai2 as monitor
import subscriber_bai1 as subscriber


def message(data, topic):
    payload = data if isinstance(data, bytes) else json.dumps(data).encode()
    return SimpleNamespace(payload=payload, topic=topic)


def output(callback, *args):
    stream = io.StringIO()
    with redirect_stdout(stream):
        callback(*args)
    return stream.getvalue()


class FakeClient:
    def __init__(self, rc=0):
        self.rc = rc
        self.published = []

    def publish(self, topic, payload):
        self.published.append((topic, json.loads(payload)))
        return SimpleNamespace(rc=self.rc)


class LabTests(unittest.TestCase):
    def test_subscriber_displays_topic_payload_time(self):
        text = output(subscriber.on_message, None, None,
                      message(b"hello", "iot/lab/message"))
        for expected in ("Topic: iot/lab/message", "Payload: hello", "Time: "):
            self.assertIn(expected, text)

    def test_sensor_alerts_and_exact_boundaries(self):
        for temperature, humidity, hot, dry in (
            (28.5, 65.2, False, False), (36.1, 65.2, True, False),
            (28.5, 38.7, False, True), (36.1, 38.7, True, True),
            (35.0, 40.0, False, False),
        ):
            with self.subTest(temperature=temperature, humidity=humidity):
                text = output(monitor.on_message, None, None, message(
                    {"device_id": "sensor01", "temperature": temperature,
                     "humidity": humidity}, "iot/lab/sensor01/data"))
                self.assertEqual("CANH BAO: Nhiet do cao" in text, hot)
                self.assertEqual("CANH BAO: Do am thap" in text, dry)

    def test_sensor_rejects_malformed_numbers_and_mismatched_topic(self):
        for data, topic in (
            (b"{bad", "iot/lab/sensor01/data"),
            (b"\xff", "iot/lab/sensor01/data"),
            ({}, "iot/lab/sensor01/data"),
            ({"device_id": "sensor01", "temperature": True, "humidity": 50}, "iot/lab/sensor01/data"),
            ({"device_id": "sensor01", "temperature": float("nan"), "humidity": 50}, "iot/lab/sensor01/data"),
            ({"device_id": "sensor01", "temperature": 25, "humidity": 101}, "iot/lab/sensor01/data"),
            ({"device_id": "sensor01", "temperature": 25, "humidity": 50}, "iot/lab/sensor02/data"),
        ):
            with self.subTest(data=data, topic=topic):
                text = output(monitor.on_message, None, None, message(data, topic))
                self.assertIn("Du lieu khong hop le:", text)
                self.assertNotIn("Temperature:", text)

    def test_sensor02_is_supported(self):
        self.assertEqual(monitor.parse_sensor_data(json.dumps(
            {"device_id": "sensor02", "temperature": 25, "humidity": 60}
        ).encode()), ("sensor02", 25.0, 60.0))

    def test_controller_commands(self):
        for text, expected in (
            ("ON", ("light01", "ON")), (" off ", ("light01", "OFF")),
            ("fan01 on", ("fan01", "ON")), ("pump01 OFF", ("pump01", "OFF")),
            ("exit", None),
        ):
            with self.subTest(text=text):
                self.assertEqual(controller.parse_command(text), expected)
        self.assertEqual(controller.parse_command("ON", "fan01"), ("fan01", "ON"))

    def test_controller_rejects_invalid_commands(self):
        for text in ("", "BLINK", "unknown ON", "light01 EXIT", "ON OFF ON"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                controller.parse_command(text)

    def test_controller_rejects_unrelated_or_inconsistent_json(self):
        for data, topic in (
            ({"unrelated": "payload"}, "iot/lab/light01/status"),
            ([], "iot/lab/light01/status"),
            ({"device_id": "light01", "status": "BROKEN"}, "iot/lab/light01/status"),
            ({"device_id": "light01", "status": "ON"}, "iot/lab/fan01/status"),
        ):
            with self.subTest(data=data, topic=topic):
                text = output(controller.on_message, None, None, message(data, topic))
                self.assertIn("Trang thai khong hop le:", text)
                self.assertNotIn("Trang thai nhan duoc:", text)

    def test_controller_displays_valid_status_for_each_device(self):
        for device_id in controller.DEVICE_IDS:
            data = {"device_id": device_id, "status": "ON"}
            text = output(controller.on_message, None, None, message(
                data, f"iot/lab/{device_id}/status"))
            self.assertIn(json.dumps(data, separators=(",", ":")), text)

    def setUp(self):
        device.DEVICE_STATES.clear()
        device.DEVICE_STATES.update({name: "OFF" for name in device.DEVICE_IDS})

    def test_device_responds_after_every_valid_command(self):
        client = FakeClient()
        for device_id in device.DEVICE_IDS:
            for command in ("ON", "ON", "OFF"):
                before = len(client.published)
                output(device.on_message, client, None, message(
                    command.encode(), f"iot/lab/{device_id}/cmd"))
                self.assertEqual(len(client.published), before + 1)
                self.assertEqual(client.published[-1], (
                    f"iot/lab/{device_id}/status",
                    {"device_id": device_id, "status": command}))

    def test_device_invalid_command_preserves_state(self):
        client = FakeClient()
        text = output(device.on_message, client, None, message(
            b"BLINK", "iot/lab/light01/cmd"))
        self.assertEqual(device.DEVICE_STATES["light01"], "OFF")
        self.assertFalse(client.published)
        self.assertIn("Lenh khong hop le", text)

    def test_device_does_not_report_success_when_publish_fails(self):
        text = output(device.publish_status, FakeClient(rc=4))
        self.assertIn("Gui trang thai that bai", text)
        self.assertNotIn("Yeu cau gui trang thai:", text)
        self.assertNotIn("Da gui trang thai:", text)


if __name__ == "__main__":
    unittest.main()
