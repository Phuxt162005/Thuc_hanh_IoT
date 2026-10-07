"""Bai 1: gui loi chao len iot/lab/message moi 3 giay."""
import argparse
import sys

from mqtt_common import MQTTConnection, add_connection_arguments, non_negative_int, run

TOPIC = "iot/lab/message"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add_connection_arguments(parser)
    parser.add_argument("--student-name", required=True, help="Ho ten sinh vien.")
    parser.add_argument("--student-id", required=True, help="Ma sinh vien.")
    parser.add_argument("--count", type=non_negative_int, default=0,
                        help="So message; 0 la gui lien tuc den Ctrl+C.")
    args = parser.parse_args()
    message = (f"Xin chao tu client Python MQTT - "
               f"{args.student_id} - {args.student_name}")
    with MQTTConnection(args.host, args.port) as connection:
        sent = 0
        while True:
            connection.publish(TOPIC, message)
            print(f"Da gui [{TOPIC}]: {message}", flush=True)
            sent += 1
            if args.count and sent >= args.count:
                break
            if connection.stopped.wait(3):
                raise RuntimeError("Broker da ngat ket noi.")


if __name__ == "__main__":
    sys.exit(run(main))
