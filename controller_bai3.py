import json
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883

CMD_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Controller da ket noi MQTT Broker.")
        client.subscribe(STATUS_TOPIC)
        print(f"Da subscribe: {STATUS_TOPIC}")
    else:
        print(f"Ket noi that bai, ma loi: {rc}")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))

        print("\nTrang thai nhan duoc:")
        print(json.dumps(data, separators=(",", ":")))

    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Trang thai nhan duoc khong phai JSON hop le.")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_start()

    while True:
        command = input("\nNhap lenh (ON/OFF/EXIT): ").strip().upper()

        if command == "EXIT":
            print("Ket thuc Controller.")
            break

        if command not in ("ON", "OFF"):
            print("Lenh khong hop le. Chi duoc nhap ON, OFF hoac EXIT.")
            continue

        result = client.publish(CMD_TOPIC, command)

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Da gui lenh {command} toi light01")
        else:
            print(f"Gui lenh that bai, ma loi: {result.rc}")

finally:
    client.loop_stop()
    client.disconnect()
