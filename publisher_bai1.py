import paho.mqtt.client as mqtt
import time

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iot/lab/message"

STUDENT_ID = "B23DCCN651"    
STUDENT_NAME = "Bui Hong Phu"


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Da ket noi MQTT Broker.")
    else:
        print(f"Ket noi that bai, ma loi: {rc}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

try:
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_start()

    message = (f"Xin chao tu client Python MQTT - " f"{STUDENT_ID} - {STUDENT_NAME}")

    while True:
        result = client.publish(TOPIC, message)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Da gui: {message}")
        else:
            print(f"Gui message that bai, ma loi: {result.rc}")

        time.sleep(3)

except KeyboardInterrupt:
    print("\nDung Publisher.")
finally:
    client.loop_stop()
    client.disconnect()
