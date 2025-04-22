# 🥫 API Pantry - Định danh sản phẩm qua ảnh sử dụng YOLO

API này sử dụng mô hình YOLO12x được huấn luyện sẵn để phát hiện các mặt hàng thường thấy trong nhà bếp (ví dụ: bánh, sữa, mì, cháo, fami, oishi...). Kết quả trả về gồm tên mặt hàng, độ chính xác và giá tiền tương ứng, cùng với tổng chi phí các mặt hàng trong ảnh.

---

## 🚀 Mô hình đã huấn luyện

🔗 [Tải file `best.pt` từ Google Drive (113MB)](https://drive.google.com/file/d/1DcpLGqtxU2aGA92R_EFn7e1vEtYdYJFH/view?usp=drive_link)

**Sau khi tải về**, đặt file `best.pt` vào thư mục gốc của project, cùng với `api_pantry.py`.

---

## 📦 Cài đặt

```bash
# Tạo môi trường ảo (tuỳ chọn)
python -m venv .venv
source .venv/bin/activate  # Đối với Linux/macOS
# hoặc
.venv\Scripts\activate      # Đối với Windows

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

---

## 📸 Sử dụng

### 1. Chạy API

```bash
uvicorn api_pantry:app --reload
```

Mặc định server sẽ chạy tại: `http://127.0.0.1:8000`

### 2. Kết quả trả về

```json
{
  "detections": [
    {
      "class_name": "banh",
      "confidence": 0.92,
      "price": 4000
    },
    {
      "class_name": "sua",
      "confidence": 0.87,
      "price": 7000
    }
  ],
  "total_price": 11000,
  "execution_time": "0.55 seconds"
}
```

---

## 🧠 Danh sách sản phẩm & giá

| Tên sản phẩm | Giá tiền (VNĐ) |
|--------------|----------------|
| banh         | 4,000          |
| sua          | 7,000          |
| fami         | 4,000          |
| mi           | 7,000          |
| chao         | 5,000          |
| oishi        | 5,000          |

---

## 🛠 Kiến trúc hệ thống

- **Framework:** FastAPI
- **Model Detection:** YOLO12x (qua thư viện `ultralytics`)
- **Xử lý ảnh:** OpenCV
- **Ghi log:** `logging`
- **Ảnh hỗ trợ:** JPG, PNG (HEIC cần chuyển đổi thành JPG or PNG)

---

## 📁 Cấu trúc thư mục

```
api_pantry/
├── api_pantry.py         # FastAPI server chính
├── best.pt               # File YOLOv8 đã huấn luyện
├── detection_results.log # file log
├── temp_uploads/         # Thư mục lưu ảnh tạm
├── requirements.txt      # Danh sách thư viện
└── README.md             # File mô tả project
```

---

## 👩‍💻 Tác giả

**Tô Văn Tú**  
Custom Object Detection API using YOLO12x + FastAPI

---

## 📜 Giấy phép

Phát hành theo giấy phép MIT (MIT License).
