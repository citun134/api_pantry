import os
import uuid
import time
import aiofiles
import logging
from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from ultralytics import YOLO
import json

best_yolo = r'model/yolo12n/best.pt'
# image_path = r"D:\PyCharm\pythonProject\yolo_api_pantry\IMG_1264_image_017.jpg"

def run_yolo_inference(model_path: str, image_path: str):
    model = YOLO(model_path)
    results = model.predict(image_path)
    json_results = []

    # Bảng giá theo tên class
    price_map = {
        "banh": 4000,
        "sua": 7000,
        "fami": 4000,
        "mi": 7000,
        "chao": 5000,
        "oishi": 5000
    }

    total_price = 0  # Biến để tính tổng

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            class_name = result.names[class_id]
            confidence = float(box.conf.item())
            coords = list(map(float, box.xyxy[0].tolist()))  # [x1, y1, x2, y2]

            # Lấy giá theo class_name, nếu không có thì gán 0
            price = price_map.get(class_name.lower(), 0)
            total_price += price

            json_results.append({
                "class_name": class_name,
                "confidence": confidence,
                "price": price
            })

    return {
        "detections": json_results,
        "total_price": total_price
    }


# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Thêm file log ghi kết quả
LOG_FILE = "detection_results.log"

# Khởi tạo app và model
app = FastAPI(title="Face Detection API", description="API phát hiện gian lận qua khuôn mặt", version="1.0")

# Middleware CORS nếu cần mở rộng hệ thống sau này
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thư mục lưu tạm ảnh upload
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Giao diện HTML đơn giản cho test
@app.get("/", response_class=HTMLResponse)
async def main():
    return """
    <html>
        <head><title>Upload Image</title></head>
        <body>
            <h2>Upload an image</h2>
            <form action="/detect" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept="image/*">
                <input type="submit" value="Upload and Detect">
            </form>
        </body>
    </html>
    """

# API phát hiện gian lận/khuôn mặt từ ảnh
@app.post("/detect", summary="Phát hiện gian lận qua ảnh", description="Nhận ảnh và phát hiện đồ ăn")
async def detect_face(request: Request, file: UploadFile = File(...)):
    # Kiểm tra định dạng ảnh
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg", "image/HEIC"]:
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ ảnh JPEG hoặc PNG.")

    # Tạo tên file tạm duy nhất
    file_ext = os.path.splitext(file.filename)[1]
    temp_filename = f"{uuid.uuid4()}{file_ext}"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)

    try:
        # Ghi file async
        async with aiofiles.open(temp_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        # Gọi model
        start_time = time.time()
        # result = run_yolo_inference(best_yolo, temp_path)
        detections = run_yolo_inference(best_yolo, temp_path)
        result = {
            "items": detections,
        }
        end_time = time.time()

        result["execution_time"] = f"{end_time - start_time:.2f} seconds"

        # Ghi log xử lý
        log_message = f"File '{file.filename}' xử lý trong {end_time - start_time:.2f}s | Kết quả: {result}\n"
        logger.info(log_message)
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(log_message)
        # file_handler = logging.FileHandler("detection_results.log", encoding="utf-8")
        # file_handler.setLevel(logging.INFO)
        # logger.addHandler(file_handler)

        return JSONResponse(content=result)

    except Exception as e:
        logger.error(f"Lỗi xử lý file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail="Lỗi trong quá trình xử lý ảnh")

    finally:
        # Xoá file tạm
        if os.path.exists(temp_path):
            os.remove(temp_path)
