from ultralytics import YOLO

# Tải mô hình YOLOv11 phân đoạn
model = YOLO("yolo11n-seg.pt")  # Mô hình nhẹ

if __name__ == "__main__":
    # Huấn luyện
    model.train(
        data="E:/Niên Luận Ngành/crab_color/data.yaml",
        epochs=100,
        imgsz=640,
        batch=32,
        name="n_color_32",
        patience=10,  # Dừng nếu không cải thiện sau 10 epoch
    )

    # Lưu mô hình
    model.save("n_color_32.pt")
    
    model.train(
        data="E:/Niên Luận Ngành/crab_grayscale/data.yaml",
        epochs=100,
        imgsz=640,
        batch=32,
        name="n_grayscale_32",
        patience=10,  # Dừng nếu không cải thiện sau 10 epoch
    )

    # Lưu mô hình
    model.save("n_color_32.pt")
