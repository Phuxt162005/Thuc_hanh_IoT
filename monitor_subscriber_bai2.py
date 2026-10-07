"""Bai 2: theo doi sensor01/sensor02 va canh bao theo nguong."""
import argparse
import json
import math
import sys
from datetime import datetime

from mqtt_common import MQTTConnection, add_connection_arguments, run

TOPIC = "iot/lab/+/data"
DEVICE_IDS = ("sensor01", "sensor02")


def parse_sensor_data(payload):
    data = json.loads(payload.decode("utf-8"))
    if not isinstance(data, dict) or data.get("device_id") not in DEVICE_IDS:
        raise ValueError("device_id phai la sensor01 hoac sensor02.")
    values = []
    for field in ("temperature", "humidity"):
        value = data[field]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{field} phai la so.")
        if not math.isfinite(value):
            raise ValueError(f"{field} phai la so huu han.")
        values.append(float(value))
    if not 0 <= values[1] <= 100:
        raise ValueError("humidity phai nam trong khoang 0..100.")
    return data["device_id"], *values


def on_message(client, userdata, msg):
    try:
        device_id, temperature, humidity = parse_sensor_data(msg.payload)
        if msg.topic != f"iot/lab/{device_id}/data":
            raise ValueError("device_id khong khop topic.")
        print(f"\n--- SENSOR DATA [{datetime.now():%H:%M:%S}] ---")
        print(f"Device: {device_id}")
        print(f"Temperature: {temperature:.1f} C")
        print(f"Humidity: {humidity:.1f} %")
        if temperature > 35:
            print("CANH BAO: Nhiet do cao")
        if humidity < 40:
            print("CANH BAO: Do am thap")
        print(flush=True)
    except (ValueError, KeyError, TypeError) as error:
        print(f"Du lieu khong hop le: {error}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add_connection_arguments(parser)
    args = parser.parse_args()
    with MQTTConnection(args.host, args.port, TOPIC, on_message) as connection:
        print("Dang theo doi sensor01/sensor02. Nhan Ctrl+C de dung.", flush=True)
        connection.wait()


if __name__ == "__main__":
    sys.exit(run(main))
