"""Bai 2: mo phong cam bien gui JSON moi 3 giay."""
import argparse
import json
import random
import sys
from datetime import datetime

from mqtt_common import MQTTConnection, add_connection_arguments, non_negative_int, run

DEVICE_IDS = ("sensor01", "sensor02")
# Binh thuong, nhiet do cao, do am thap, ca hai canh bao, dung bien.
DEMO_VALUES = ((28.5, 65.2), (36.1, 65.2), (28.5, 38.7),
               (36.1, 38.7), (35.0, 40.0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add_connection_arguments(parser)
    parser.add_argument("--device-id", choices=DEVICE_IDS, default="sensor01")
    parser.add_argument("--all-devices", action="store_true",
                        help="Gui du lieu cua ca sensor01 va sensor02.")
    parser.add_argument("--demo", action="store_true",
                        help="Dung 5 cap gia tri biet truoc thay cho ngau nhien.")
    parser.add_argument("--count", type=non_negative_int, default=0,
                        help="So chu ky gui; 0 la chay den Ctrl+C.")
    args = parser.parse_args()
    devices = DEVICE_IDS if args.all_devices else (args.device_id,)
    with MQTTConnection(args.host, args.port) as connection:
        cycle = 0
        while True:
            for device_id in devices:
                if args.demo:
                    temperature, humidity = DEMO_VALUES[cycle % len(DEMO_VALUES)]
                else:
                    temperature = round(random.uniform(20.0, 40.0), 1)
                    humidity = round(random.uniform(30.0, 80.0), 1)
                data = {"device_id": device_id, "temperature": temperature,
                        "humidity": humidity}
                topic = f"iot/lab/{device_id}/data"
                payload = json.dumps(data)
                connection.publish(topic, payload)
                print(f"[{datetime.now():%H:%M:%S}] Gui [{topic}]: {payload}", flush=True)
            cycle += 1
            if args.count and cycle >= args.count:
                break
            if connection.stopped.wait(3):
                raise RuntimeError("Broker da ngat ket noi.")


if __name__ == "__main__":
    sys.exit(run(main))
