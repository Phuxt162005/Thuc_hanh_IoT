import json
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iot/lab/sensor01/data"


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Monitoring Subscriber da ket noi MQTT Broker.")
        client.subscribe(TOPIC)
        print(f"Da subscribe: {TOPIC}")
    else:
        print(f"Ket noi that bai, ma loi: {rc}")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))

        device_id = data["device_id"]
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])

        print("\n--- SENSOR DATA ---")
        print(f"Device: {device_id}")
        print(f"Temperature: {temperature:.1f} C")
        print(f"Humidity: {humidity:.1f} %")

        if temperature > 35:
            print("CANH BAO: Nhiet do cao")

        if humidity < 40:
            print("CANH BAO: Do am thap")

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f"Du lieu khong hop le: {e}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    print("Monitoring Subscriber dang cho du lieu... Nhan Ctrl+C de dung.")
    client.loop_forever()

except KeyboardInterrupt:
    print("\nDung Monitoring Subscriber.")
finally:
    client.disconnect()
