# Phân Loại Kích Cỡ Cua Biển Tự Động Sử Dụng YOLOv11n-seg: Nghiên Cứu Tại Ngành Nuôi Trồng Thủy Sản Việt Nam

## Tóm tắt
Nghiên cứu này giới thiệu một hệ thống tự động phân loại kích cỡ cua biển sử dụng mô hình YOLOv11n-seg, nhằm nâng cao hiệu quả trong ngành nuôi trồng thủy sản Việt Nam, đặc biệt tại khu vực Đồng bằng sông Cửu Long. Hệ thống tận dụng thiết bị ESP32-CAM giá rẻ để thu thập ảnh và Raspberry Pi 4 để xử lý, đạt hiệu suất thời gian thực với độ chính xác 97,8% và thời gian xử lý dưới 100ms mỗi ảnh. Mô hình được huấn luyện trên tập dữ liệu gồm 720 ảnh, đạt các chỉ số cao (mAP@0.5 cho mask: 0,9945; F1-score: 0,99). Tuy nhiên, hệ thống còn hạn chế trong việc phát hiện lớp nền và nhạy cảm với điều kiện môi trường. Các khuyến nghị bao gồm mở rộng tập dữ liệu và tối ưu hóa phân loại đa góc.

## 1. Giới thiệu

Ngành nuôi trồng thủy sản Việt Nam, đặc biệt tại Đồng bằng sông Cửu Long, là một trụ cột kinh tế, với sản lượng cua biển (Scylla serrata) tại Trà Vinh đạt 6.667 tấn mỗi năm (2023). Việc phân loại kích cỡ cua chính xác là yếu tố quan trọng đối với thị trường xuất khẩu, nơi giá trị chênh lệch theo kích cỡ có thể lên đến 25–40%. Phương pháp phân loại thủ công hiện nay tốn thời gian, chi phí lao động cao và dễ xảy ra sai sót. Nghiên cứu này đề xuất một hệ thống sử dụng YOLOv11n-seg để tự động hóa quá trình phân loại kích cỡ cua, nhằm giảm chi phí lao động và tăng độ chính xác. Mục tiêu bao gồm phát triển hệ thống thời gian thực, tối ưu hóa hiệu quả và nâng cao giá trị sản phẩm xuất khẩu.

## 2. Phương pháp nghiên cứu

### 2.1 Thu thập và xử lý dữ liệu

Tập dữ liệu gồm 720 ảnh được thu thập bằng thiết bị ESP32-CAM tại các trang trại cua ở Trà Vinh và Cà Mau. Ảnh được chụp trong điều kiện ánh sáng kiểm soát (khoảng cách 30–40 cm, hỗ trợ đèn LED) và xử lý như sau:
![Setup](images/setup.png)
- Điều chỉnh kích thước ảnh về 640×640 pixel.
- Gán nhãn bằng công cụ LabelMe cho phân đoạn (lớp: Crab, Reference).
- Tăng cường dữ liệu thông qua xoay, lật và điều chỉnh độ sáng.

### 2.2 Kiến trúc mô hình

Hệ thống sử dụng YOLOv11n-seg để nhận diện và phân đoạn, triển khai trên Raspberry Pi 4. ESP32-CAM thu thập ảnh và truyền qua WiFi để xử lý. Các bước chính:

1. Phân đoạn vùng mai cua và vật tham chiếu (20×20 mm) bằng YOLOv11n-seg.
2. Tính toán chiều rộng mai cua dựa trên vật tham chiếu.
3. Phân loại cua vào các hạng kích cỡ (Y7, Y5, Y3, Y4, Xô) dựa trên chiều rộng mai.

### 2.3 Huấn luyện mô hình

Mô hình được huấn luyện trên GPU NVIDIA RTX 3060, sử dụng PyTorch và Ultralytics CLI:

- **Phân chia dữ liệu**: 88% huấn luyện, 8% xác thực, 4% kiểm tra.
- **Tham số huấn luyện**: Batch size 32, 100 epoch, tối ưu hóa bằng Adam, tỷ lệ học tự động.
- **Chỉ số đánh giá**: IoU, mAP@0.5, mAP@0.5:0.95, Precision, Recall, F1-score.

## 3. Kết quả

### 3.1 Hiệu suất mô hình

Hai mô hình được đánh giá: mô hình ảnh màu và mô hình ảnh xám.

- **Mô hình ảnh màu**:
  - mAP@0.5 (Mask): 0,9945; mAP@0.5:0.95: 0,91569.
  - Precision/Recall (Crab): 1,0; F1-score: 1,0.
  - Độ chính xác tổng thể: 97,8%.
  - Thời gian xử lý: &lt;100ms/ảnh.
- **Mô hình ảnh xám**:
  - mAP@0.5 (Mask): 0,98522; mAP@0.5:0.95: 0,74391.
  - Precision/Recall (Crab): 0,95/1,0; F1-score: 0,9744.
  - Độ chính xác tổng thể: 94,6%. Mô hình ảnh màu vượt trội hơn, đặc biệt trong việc phân biệt cua với nền.

### 3.2 Phân tích mất mát (Loss)

- **Mô hình ảnh màu**:
  - Train Box Loss: Giảm từ 1,2 xuống 0,4.
  - Train Segmentation Loss: Giảm từ 2,73 xuống 0,4.
- **Mô hình ảnh xám**:
  - Train Box Loss: Giảm từ 1,45 xuống 0,52.
  - Train Segmentation Loss: Giảm từ 2,93 xuống 0,68. Mô hình ảnh màu cho thấy sự hội tụ ổn định hơn và mức mất mát thấp hơn.

### 3.3 Ma trận nhầm lẫn (Confusion Matrix)

- **Mô hình ảnh màu**:
  - Crab: Precision 1,0, Recall 1,0.
  - Reference: Precision 0,9355, Recall 1,0.
  - Background: Recall 0,0 (do mất cân bằng dữ liệu: chỉ có 2 mẫu nền).
- **Mô hình ảnh xám**:
  - Crab: Precision 0,95, Recall 1,0.
  - Background: Recall 0,0 (6 mẫu bị phân loại sai).

### 3.4 Kiểm thử

Mô hình ảnh màu được kiểm thử trong điều kiện thực tế:

- IoU cho phân đoạn cua: 0,89–0,92.
- Độ chính xác phân loại kích cỡ: Bị ảnh hưởng bởi sai số đo lường (sai số tương đối 23,5%), dẫn đến phân loại không nhất quán (ví dụ: một con cua bị phân loại thành Y5, Y3 và Y4).

## 4. Thảo luận

Hệ thống cho thấy tiềm năng lớn trong việc tự động hóa phân loại kích cỡ cua, với độ chính xác cao và xử lý thời gian thực. Tuy nhiên, vẫn tồn tại các thách thức:

- Hiệu suất kém với lớp nền do mất cân bằng dữ liệu.
- Nhạy cảm với điều kiện ánh sáng và tư thế cua.
- Sai số đo lường gần ngưỡng phân loại (ví dụ: 10,9 cm so với 11 cm). Các khuyến nghị bao gồm:
- Thu thập tập dữ liệu lớn hơn, đa dạng hơn (10.000+ ảnh).
- Triển khai chụp ảnh đa góc và tái tạo 3D.
- Điều chỉnh ngưỡng phân loại để giảm sai số.

## 5. Kết luận

Hệ thống dựa trên YOLOv11n-seg đã thành công trong việc tự động hóa phân loại kích cỡ cua biển, đạt độ chính xác 97,8% và hiệu suất thời gian thực. Đây là một giải pháp tiết kiệm chi phí cho ngành thủy sản Việt Nam, giúp giảm chi phí lao động và nâng cao giá trị xuất khẩu. Các nghiên cứu tiếp theo cần tập trung vào việc cải thiện khả năng xử lý các điều kiện môi trường khác nhau và tích hợp thêm các chỉ số chất lượng cua.

## Lời cảm ơn

Nghiên cứu này nhận được sự hỗ trợ từ các hộ nuôi cua tại Trà Vinh và Cà Mau, những người đã cung cấp quyền truy cập vào trang trại và chia sẻ thông tin quý giá về thách thức trong phân loại thủ công.