from ultralytics import YOLO
import cv2
import os
import numpy as np
import csv

# Đường dẫn tới mô hình đã huấn luyện
# model_path = "E:/Crab_Segmentation_Yolov11/model/dataset_color/best.pt"
model_path = "E:/Crab_Segmentation_Yolov11/model/dataset_grayscale/best.pt"
model = YOLO(model_path)

# Thư mục đầu vào (chứa ảnh cần xử lý)
input_folder = "D:/Test"

# Thư mục đầu ra (nơi lưu ảnh đã xử lý)
output_folder = "E:/Crab_Segmentation_Yolov11/outimages"

# Đường dẫn file CSV
csv_path = os.path.join(output_folder, "area_results.csv")

# Tạo thư mục đầu ra nếu chưa tồn tại
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# Hàm xử lý và lưu ảnh
def process_and_save_image(image_path, output_path):
    # img = cv2.imread(image_path)  # Đọc ảnh màu trực tiếp
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Đọc ảnh xám trực tiếp
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)# Dùng cho model ảnh xám

    results = model(img, conf=0.25)
    result = results[0]
    annotated_img = img.copy()
    csv_data = []

    if result.boxes is not None and result.masks is not None:
        for box, mask, cls in zip(
            result.boxes.xyxy, result.masks.data, result.boxes.cls
        ):
            x1, y1, x2, y2 = map(int, box)
            class_id = int(cls)
            class_name = result.names[class_id]
            mask = mask.cpu().numpy()
            mask = cv2.resize(mask, (annotated_img.shape[1], annotated_img.shape[0]))
            area = np.sum(mask > 0.5)
            color = (0, 255, 0) if class_id == 0 else (0, 0, 255)

            # Vẽ hộp bao quanh đối tượng
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), color, 2)

            # Tô màu mask
            mask_color = np.zeros_like(annotated_img)
            mask_color[mask > 0.5] = color
            annotated_img = cv2.addWeighted(annotated_img, 0.7, mask_color, 0.3, 0)

            # Lưu thông tin vào CSV
            csv_data.append(
                {
                    "image_name": os.path.basename(image_path),
                    "class_name": class_name,
                    "area_pixels": area,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                }
            )

    cv2.imwrite(output_path, annotated_img)
    print(f"Đã xử lý và lưu ảnh tại: {output_path}")
    return csv_data


# Xử lý tất cả ảnh
all_results = []
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"processed_{filename}")
        results = process_and_save_image(input_path, output_path)
        all_results.extend(results)

# Lưu kết quả vào CSV
if all_results:
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["image_name", "class_name", "area_pixels", "x1", "y1", "x2", "y2"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in all_results:
            writer.writerow(result)
    print(f"Đã lưu kết quả diện tích vào: {csv_path}")
else:
    print("Không có kết quả để lưu vào CSV")

print("Đã hoàn tất xử lý tất cả ảnh!")
