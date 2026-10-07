"""Bai 1: nhan topic, payload va thoi diem nhan; Ctrl+C de dung."""
import argparse
import sys
from datetime import datetime

from mqtt_common import MQTTConnection, add_connection_arguments, run

TOPIC = "iot/lab/message"


def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8", errors="replace")
    print("\nNhan duoc message:")
    print(f"Topic: {msg.topic}")
    print(f"Payload: {payload}")
    print(f"Time: {datetime.now():%H:%M:%S}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add_connection_arguments(parser)
    args = parser.parse_args()
    with MQTTConnection(args.host, args.port, TOPIC, on_message) as connection:
        print("Dang cho message. Nhan Ctrl+C de dung.", flush=True)
        connection.wait()


if __name__ == "__main__":
    sys.exit(run(main))
