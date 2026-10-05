import paho.mqtt.client as mqtt
from datetime import datetime

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iot/lab/message"


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Da ket noi MQTT Broker.")
        client.subscribe(TOPIC)
        print(f"Da subscribe: {TOPIC}")
    else:
        print(f"Ket noi that bai, ma loi: {rc}")


def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8", errors="replace")
    received_time = datetime.now().strftime("%H:%M:%S")

    print("\nNhan duoc message:")
    print(f"Topic: {msg.topic}")
    print(f"Payload: {payload}")
    print(f"Time: {received_time}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    print("Subscriber dang cho message... Nhan Ctrl+C de dung.")
    client.loop_forever()

except KeyboardInterrupt:
    print("\nDung Subscriber.")
finally:
    client.disconnect()
