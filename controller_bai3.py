"""Bai 3: gui ON/OFF va hien thi phan hoi cua light01/fan01/pump01."""
import argparse
import json
import sys

from mqtt_common import MQTTConnection, add_connection_arguments, run

DEVICE_IDS = ("light01", "fan01", "pump01")
STATUS_TOPIC = "iot/lab/+/status"


def parse_command(text, default_device="light01"):
    parts = text.strip().split()
    if len(parts) == 1 and parts[0].upper() == "EXIT":
        return None
    if len(parts) == 1:
        device_id, command = default_device, parts[0].upper()
    elif len(parts) == 2:
        device_id, command = parts[0].lower(), parts[1].upper()
    else:
        raise ValueError("Nhap ON/OFF, <device_id> ON/OFF hoac EXIT.")
    if device_id not in DEVICE_IDS or command not in ("ON", "OFF"):
        raise ValueError("Thiet bi: light01/fan01/pump01; lenh: ON/OFF.")
    return device_id, command


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Payload trang thai phai la JSON object.")
        device_id = data.get("device_id")
        if device_id not in DEVICE_IDS or data.get("status") not in ("ON", "OFF"):
            raise ValueError("device_id hoac status khong hop le.")
        if msg.topic != f"iot/lab/{device_id}/status":
            raise ValueError("device_id khong khop topic.")
        print("\nTrang thai nhan duoc:")
        print(json.dumps(data, separators=(",", ":")), flush=True)
    except (ValueError, TypeError) as error:
        print(f"Trang thai khong hop le: {error}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add_connection_arguments(parser)
    parser.add_argument("--device-id", choices=DEVICE_IDS, default="light01",
                        help="Thiet bi nhan lenh ON/OFF khong kem device_id.")
    args = parser.parse_args()
    with MQTTConnection(args.host, args.port, STATUS_TOPIC, on_message) as connection:
        print("Nhap ON/OFF cho thiet bi mac dinh; fan01 ON, pump01 OFF; EXIT de dung.",
              flush=True)
        while True:
            text = input(f"\nNhap lenh [{args.device_id}]: ")
            try:
                parsed = parse_command(text, args.device_id)
            except ValueError as error:
                print(f"Lenh khong hop le: {error}", flush=True)
                continue
            if parsed is None:
                break
            device_id, command = parsed
            connection.publish(f"iot/lab/{device_id}/cmd", command)
            print(f"Da gui lenh {command} toi {device_id}; cho phan hoi.", flush=True)


if __name__ == "__main__":
    sys.exit(run(main))
