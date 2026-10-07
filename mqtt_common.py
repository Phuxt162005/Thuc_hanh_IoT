"""Ket noi MQTT va tham so dung chung cho sau chuong trinh."""
import argparse
import sys
from threading import Event

import paho.mqtt.client as mqtt

CONNECT_TIMEOUT = 5
PUBLISH_TIMEOUT = 5


def port_number(value):
    port = int(value)
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("Port phai nam trong khoang 1..65535.")
    return port


def non_negative_int(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("Gia tri phai >= 0.")
    return number


def add_connection_arguments(parser):
    parser.add_argument("--host", default="127.0.0.1", help="Dia chi broker.")
    parser.add_argument("--port", type=port_number, default=1884, help="Cong broker.")


class MQTTConnection:
    """Cho CONNACK/SUBACK truoc khi chuong trinh bat dau lam viec."""

    def __init__(self, host, port, topic=None, on_message=None):
        self.host, self.port, self.topic = host, port, topic
        self.ready = Event()
        self.stopped = Event()
        self.error = None
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                                  reconnect_on_failure=False)
        self.client.connect_timeout = CONNECT_TIMEOUT
        self.client.on_connect = self._on_connect
        self.client.on_subscribe = self._on_subscribe
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = on_message

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code != 0:
            self.error = f"Broker tu choi ket noi: {reason_code}"
            self.ready.set()
            return
        if self.topic:
            result, _ = client.subscribe(self.topic)
            if result != mqtt.MQTT_ERR_SUCCESS:
                self.error = f"Khong gui duoc yeu cau subscribe: {result}"
                self.ready.set()
        else:
            self.ready.set()

    def _on_subscribe(self, client, userdata, mid, reason_codes, properties):
        if any(code.is_failure for code in reason_codes):
            self.error = "Broker tu choi subscribe."
        self.ready.set()

    def _on_disconnect(self, client, userdata, flags, reason_code, properties):
        if reason_code != 0:
            print(f"Mat ket noi broker: {reason_code}", file=sys.stderr, flush=True)
        self.stopped.set()

    def __enter__(self):
        try:
            self.client.connect(self.host, self.port, 60)
            self.client.loop_start()
            if not self.ready.wait(CONNECT_TIMEOUT):
                raise RuntimeError("Het thoi gian cho broker xac nhan ket noi/subscribe.")
            if self.error:
                raise RuntimeError(self.error)
            if self.stopped.is_set():
                raise RuntimeError("Broker da ngat ket noi.")
            print(f"Da ket noi broker {self.host}:{self.port}.", flush=True)
            if self.topic:
                print(f"Da subscribe: {self.topic}", flush=True)
            return self
        except OSError as error:
            self.close()
            raise RuntimeError(
                f"Khong ket noi duoc {self.host}:{self.port}. "
                "Kiem tra broker da chay va host/port. "
                f"Chi tiet: {error}"
            ) from error
        except Exception:
            self.close()
            raise

    def publish(self, topic, payload):
        result = self.client.publish(topic, payload)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(f"Gui that bai, ma loi: {result.rc}")
        result.wait_for_publish(timeout=PUBLISH_TIMEOUT)
        if not result.is_published():
            raise RuntimeError("Het thoi gian cho gui message.")
        # QoS 0 xac nhan gui tu client; ket qua o subscriber chung minh ben nhan.
        return result

    def wait(self):
        self.stopped.wait()
        raise RuntimeError("Chuong trinh dung vi broker da ngat ket noi.")

    def close(self):
        self.client.disconnect()
        self.client.loop_stop()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def run(main):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        main()
        return 0
    except (KeyboardInterrupt, EOFError):
        print("\nDung chuong trinh.", flush=True)
        return 0
    except (RuntimeError, OSError) as error:
        print(f"Loi: {error}", file=sys.stderr, flush=True)
        return 1
