import json
import random
import time
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iot/lab/sensor01/data"

DEVICE_ID = "sensor01"


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Sensor Publisher da ket noi MQTT Broker.")
    else:
        print(f"Ket noi that bai, ma loi: {rc}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

try:
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_start()

    while True:
        temperature = round(random.uniform(20.0, 40.0), 1)
        humidity = round(random.uniform(30.0, 80.0), 1)
        data = {
            "device_id": DEVICE_ID,
            "temperature": temperature,
            "humidity": humidity
        }
        payload = json.dumps(data)

        result = client.publish(TOPIC, payload)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Da gui: {payload}")
        else:
            print(f"Gui that bai, ma loi: {result.rc}")

        time.sleep(3)

except KeyboardInterrupt:
    print("\nDung Sensor Publisher.")
finally:
    client.loop_stop()
    client.disconnect()
