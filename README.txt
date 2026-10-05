# BUOI THUC HANH 1 - PYTHON VOI GIAO THUC MQTT

## 1. Gioi thieu

Bai thuc hanh gom 3 bai:

- Bai 1: MQTT Publisher / Subscriber co ban.
- Bai 2: Mo phong cam bien nhiet do va do am.
- Bai 3: Mo phong he thong dieu khien den thong minh hai chieu.

## 2. Moi truong

- Python 3.x
- Thu vien paho-mqtt
- MQTT Broker
- IDE / VS Code

Cai thu vien:

    pip install paho-mqtt

## 3. Cau hinh MQTT Broker

Mac dinh code su dung MQTT Broker chay tren may local:

    Host: localhost
    Port: 1883

Neu su dung broker khac, sua BROKER_HOST va BROKER_PORT trong cac file Python.

## 4. Cau truc file

    publisher_bai1.py
    subscriber_bai1.py
    sensor_publisher_bai2.py
    monitor_subscriber_bai2.py
    device_bai3.py
    controller_bai3.py
    README.txt

## 5. Bai 1

Topic:

    iot/lab/message

Chay Subscriber truoc:

    python subscriber_bai1.py

Sau do mo terminal khac va chay Publisher:

    python publisher_bai1.py

Publisher gui message gom ma sinh vien, ho ten va loi chao.
Subscriber hien thi Topic, Payload va thoi diem nhan.

Nhan Ctrl+C de dung chuong trinh.

## 6. Bai 2

Topic:

    iot/lab/sensor01/data

Chay Monitoring Subscriber:

    python monitor_subscriber_bai2.py

Mo terminal khac va chay Sensor Publisher:

    python sensor_publisher_bai2.py

Sensor Publisher tao nhiet do va do am ngau nhien, gui JSON moi 3 giay.

Subscriber canh bao khi:

    Nhiet do > 35 C
    Do am < 40 %

## 7. Bai 3

Topic dieu khien:

    iot/lab/light01/cmd

Topic trang thai:

    iot/lab/light01/status

Chay Device truoc:

    python device_bai3.py

Mo terminal khac va chay Controller:

    python controller_bai3.py

Nhap:

    ON

hoac:

    OFF

Controller gui lenh den device. Device thay doi trang thai va gui JSON trang thai ve Controller.

De ket thuc Controller, nhap:

    EXIT

## 8. Ket qua dat duoc

- Bai 1: Publisher va Subscriber giao tiep qua MQTT dung topic.
- Bai 2: Du lieu cam bien duoc gui dinh ky duoi dang JSON va Subscriber kiem tra nguong.
- Bai 3: Controller dieu khien Smart Light va nhan phan hoi trang thai qua MQTT.

## 9. Mo rong da cai dat

- Publisher Bai 1 gui nhieu message lien tiep.
- Subscriber chay lien tuc den khi Ctrl+C.
- Sensor Bai 2 gui du lieu dinh ky moi 3 giay.
- Monitoring Subscriber xu ly JSON va canh bao theo nguong.
- Controller Bai 3 kiem tra lenh sai.
- Controller co lenh EXIT.
- Device Bai 3 giao tiep hai chieu voi Controller.

## 10. Luu y

Hay thay STUDENT_ID va STUDENT_NAME trong publisher_bai1.py bang thong tin cua sinh vien truoc khi nop bai.
