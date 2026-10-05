import json
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883

CMD_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"

DEVICE_ID = "light01"
current_status = "OFF"


def publish_status(client):
    payload = {
        "device_id": DEVICE_ID,
        "status": current_status
    }
    client.publish(STATUS_TOPIC, json.dumps(payload))
    print(f"Da gui trang thai: {json.dumps(payload)}")


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Smart Light Device da ket noi MQTT Broker.")
        client.subscribe(CMD_TOPIC)
        print(f"Da subscribe: {CMD_TOPIC}")
    else:
        print(f"Ket noi that bai, ma loi: {rc}")


def on_message(client, userdata, msg):
    global current_status

    command = msg.payload.decode("utf-8", errors="replace").strip().upper()

    if command == "ON":
        current_status = "ON"
        print("Nhan lenh ON -> Den BAT")
        publish_status(client)

    elif command == "OFF":
        current_status = "OFF"
        print("Nhan lenh OFF -> Den TAT")
        publish_status(client)

    else:
        print(f"Lenh khong hop le: {command}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    print("Smart Light Device dang cho lenh... Nhan Ctrl+C de dung.")
    client.loop_forever()

except KeyboardInterrupt:
    print("\nDung Smart Light Device.")
finally:
    client.disconnect()
