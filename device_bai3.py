"""Bai 3: mo phong light01, fan01 va pump01 nhan ON/OFF."""
import argparse
import json
import sys

import paho.mqtt.client as mqtt
from mqtt_common import MQTTConnection, add_connection_arguments, run

DEVICE_IDS = ("light01", "fan01", "pump01")
DEVICE_STATES = {"light01": "OFF"}
CMD_TOPIC = "iot/lab/+/cmd"


def publish_status(client, device_id="light01"):
    data = {"device_id": device_id, "status": DEVICE_STATES[device_id]}
    payload = json.dumps(data)
    result = client.publish(f"iot/lab/{device_id}/status", payload)
    # Callback chay tren network thread: khong wait_for_publish tai day.
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        print(f"Gui trang thai that bai, ma loi: {result.rc}", flush=True)
        return False
    print(f"Yeu cau gui trang thai: {payload}", flush=True)
    return True


def on_message(client, userdata, msg):
    device_id = msg.topic.split("/")[-2]
    if device_id not in DEVICE_STATES:
        print(f"Bo qua lenh cho thiet bi chua mo phong: {device_id}", flush=True)
        return
    command = msg.payload.decode("utf-8", errors="replace").strip().upper()
    if command not in ("ON", "OFF"):
        print(f"Lenh khong hop le cho {device_id}: {command}", flush=True)
        return
    DEVICE_STATES[device_id] = command
    print(f"Nhan lenh {device_id} {command} -> trang thai {command}", flush=True)
    publish_status(client, device_id)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add_connection_arguments(parser)
    parser.add_argument("--device-id", choices=DEVICE_IDS, default="light01")
    parser.add_argument("--all-devices", action="store_true",
                        help="Mo phong ca light01, fan01 va pump01.")
    args = parser.parse_args()
    devices = DEVICE_IDS if args.all_devices else (args.device_id,)
    DEVICE_STATES.clear()
    DEVICE_STATES.update({device_id: "OFF" for device_id in devices})
    with MQTTConnection(args.host, args.port, CMD_TOPIC, on_message) as connection:
        print(f"Thiet bi: {', '.join(devices)}; ban dau OFF. Nhan Ctrl+C de dung.",
              flush=True)
        connection.wait()


if __name__ == "__main__":
    sys.exit(run(main))
