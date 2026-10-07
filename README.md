# Thực hành buổi 1 — Python và MQTT

Bài nộp gồm ba bài mô phỏng gửi nhận thông điệp, giám sát cảm biến và điều khiển thiết bị qua MQTT. Ảnh thực nghiệm ngày **07/10/2026** nằm trong `minh-chung/`.

## Cấu trúc repo

```text
Thuc_hanh_IoT/
├── publisher_bai1.py             # Gửi lời chào và thông tin sinh viên
├── subscriber_bai1.py            # Nhận thông điệp, in topic và thời gian
├── sensor_publisher_bai2.py       # Mô phỏng dữ liệu cảm biến dạng JSON
├── monitor_subscriber_bai2.py     # Hiển thị dữ liệu và cảnh báo
├── device_bai3.py                # Nhận lệnh và gửi trạng thái thiết bị
├── controller_bai3.py            # Nhập lệnh và nhận phản hồi
├── mqtt_common.py                # Kết nối MQTT dùng chung
├── config/mosquitto.conf         # Cấu hình broker local
├── scripts/                     # Setup môi trường và khởi động broker
├── tests/test_logic.py           # Kiểm tra logic xử lý dữ liệu, lệnh
├── requirements.txt             # Thư viện Python
├── minh-chung/                   # 10 ảnh chụp kết quả chạy
└── README.md
```

## Môi trường và broker sử dụng

| Thành phần | Cấu hình đã dùng |
|---|---|
| Hệ điều hành, terminal | Windows 11, PowerShell |
| Python | 3.13.1, môi trường ảo `.venv` |
| Thư viện MQTT | `paho-mqtt==2.1.0` |
| Broker | Eclipse Mosquitto 2.1.2, cài tại `C:\Users\os\Desktop\Tools\Mosquitto` |
| Kết nối | `127.0.0.1:1884`, không yêu cầu tài khoản, chỉ truy cập trên máy local |

Broker dùng `config/mosquitto.conf`; cổng 1884 chạy riêng với Mosquitto service ở cổng 1883. Topic là tên kênh dữ liệu trong broker, ví dụ `iot/lab/message`.

Hai script đã dùng để dựng môi trường và chạy broker:

```powershell
.\scripts\setup.ps1
.\scripts\start-broker.ps1
```

`setup.ps1` tạo `.venv` và cài thư viện từ `requirements.txt`. Python và Mosquitto đã được cài sẵn ngoài repo; `.venv` và dữ liệu setup trong `.local` được Git bỏ qua.

![Setup thành công và Mosquitto chạy trên cổng 1884](<minh-chung/bật mosquito.png>)

## Cách chạy và kết quả

Các lệnh dưới đây chạy bằng PowerShell tại thư mục repo. Broker được giữ chạy ở một terminal riêng. Với mỗi bài, chạy bên nhận trước rồi chạy bên gửi ở terminal khác; dừng các chương trình bằng **Ctrl+C**, riêng controller có lệnh **EXIT**.

### Bài 1 — Gửi và nhận thông điệp

```powershell
# Terminal nhận
.\.venv\Scripts\python.exe subscriber_bai1.py

# Terminal gửi
.\.venv\Scripts\python.exe publisher_bai1.py --student-name "Nguyen Hai Hung" --student-id "B23DCCN371"
# (hoặc: .\.venv\Scripts\python.exe publisher_bai1.py --student-name "Bui Hong Phu" --student-id "B23DCCN651")
# (hoặc: .\.venv\Scripts\python.exe publisher_bai1.py --student-name "Vu Viet Anh" --student-id "B23DCCN060")
```

**Kết quả:** publisher gửi lời chào kèm họ tên, mã sinh viên lên `iot/lab/message` mỗi 3 giây. Subscriber nhận liên tục và hiển thị đúng topic, nội dung, thời điểm nhận. Ảnh cuối ghi lại publisher dừng bằng Ctrl+C và trở về dấu nhắc PowerShell.

![Bài 1 — publisher gửi nhiều thông điệp](<minh-chung/bài 1 - publisher.png>)

![Bài 1 — subscriber hiển thị topic, payload và thời gian nhận](<minh-chung/bài 1 - subscriber.png>)

![Bài 1 — dừng publisher bằng Ctrl+C](<minh-chung/bài 1 - publisher - ngắt ctrl C.png>)

### Bài 2 — Giám sát nhiệt độ và độ ẩm

```powershell
# Terminal nhận
.\.venv\Scripts\python.exe monitor_subscriber_bai2.py
# Terminal gửi
.\.venv\Scripts\python.exe sensor_publisher_bai2.py
```

Publisher mô phỏng sensor01, gửi JSON gồm `device_id`, `temperature`, `humidity` mỗi 3 giây; nhiệt độ ngẫu nhiên 20–40°C, độ ẩm 30–80%. Monitor nhận trên `iot/lab/+/data`, hiển thị từng trường và cảnh báo khi nhiệt độ **> 35°C** hoặc độ ẩm **< 40%**.

Phần mở rộng hỗ trợ sensor02. Lệnh chạy hai cảm biến với 5 bộ dữ liệu cố định để kiểm tra các ngưỡng cảnh báo:

```powershell
.\.venv\Scripts\python.exe sensor_publisher_bai2.py --demo --all-devices --count 5
```

**Kết quả trong ảnh:** sensor01 gửi dữ liệu cách nhau 3 giây; monitor nhận và hiển thị các giá trị khớp với publisher, ví dụ **22.4°C, 73.7%** lúc **16:24:27**.

![Bài 2 — sensor01 gửi dữ liệu JSON](<minh-chung/bài 2 - sensor publisher.png>)

![Bài 2 — monitor hiển thị dữ liệu sensor01 theo từng trường](<minh-chung/bài 2 - monitor subscriber.png>)

### Bài 3 — Điều khiển thiết bị hai chiều

```powershell
# Terminal thiết bị
.\.venv\Scripts\python.exe device_bai3.py
# Terminal điều khiển
.\.venv\Scripts\python.exe controller_bai3.py
```

Controller nhận lệnh `ON`/`OFF` từ bàn phím và gửi lên `iot/lab/light01/cmd`. Device cập nhật trạng thái đèn mô phỏng rồi gửi JSON gồm `device_id`, `status` lên `iot/lab/light01/status` để controller hiển thị.

**Kết quả:** light01 phản hồi đúng `ON` và `OFF`; controller báo lệnh không hợp lệ khi nhập `HELLO`, sau đó tiếp tục nhận lệnh. Nhập `EXIT` kết thúc controller.

![Bài 3 — light01 nhận lệnh và gửi trạng thái](<minh-chung/bài 3 - device - 1 thiết bị.png>)

![Bài 3 — controller nhận phản hồi, xử lý HELLO và EXIT](<minh-chung/bài 3 - controller.png>)

**Mở rộng nhiều thiết bị:** chạy device với lệnh dưới đây và giữ cách chạy controller như trên. Lệnh có tên thiết bị, ví dụ `fan01 ON` hoặc `pump01 OFF`, dùng topic `iot/lab/<device_id>/cmd`; phản hồi ở `iot/lab/<device_id>/status`.

```powershell
.\.venv\Scripts\python.exe device_bai3.py --all-devices
```

**Kết quả trong ảnh:** light01 nhận `ON`/`OFF`, fan01 nhận `ON`/`OFF`, pump01 nhận `OFF`; controller hiển thị phản hồi đúng tên thiết bị và trạng thái.

![Bài 3 — device xử lý light01, fan01 và pump01](<minh-chung/bài 3 - device - nhiều thiết bị.png>)

![Bài 3 — controller hiển thị phản hồi của nhiều thiết bị](<minh-chung/bài 3 - controller - xử lý nhiều thiết bị.png>)
