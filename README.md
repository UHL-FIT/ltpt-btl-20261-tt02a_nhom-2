# EzGrade - Hệ Thống Chấm Điểm Trắc Nghiệm

**EzGrade** là một ứng dụng Python chuyên trợ giúp giáo viên/người dùng quản lý đề thi, thông tin thí sinh, tự động chấm điểm bài thi trắc nghiệm và phân tích thống kê kết quả một cách trực quan, hiện đại.

**Lưu ý quan trọng** : Đây là dự án ví dụ cốt lõi (cơ bản) dành cho sinh viên tham khảo trong quá trình phát triển và hoàn thiện Bài tập lớn môn Lập trình Python. Mọi tính năng cơ bản của một ứng dụng quản lý đều được phát triển theo tiêu chuẩn.

## Tính năng
- **Quản lý Đề thi** : Thêm, Chỉnh sửa, Xóa và Tìm kiếm linh hoạt. Hỗ trợ nhập và xuất hàng loạt dữ liệu đề thi qua tệp .csv. Lưới đáp án linh hoạt theo số câu.
- **Quản lý Thí sinh & Chấm điểm** : Thêm, sửa, xóa thông tin thí sinh, nhập nhanh bài làm. Chấm điểm tự động dựa trên đáp án chuẩn với tốc độ tối ưu nhờ sử dụng Numpy.
- **Thống kê Trực quan** : Phân tích và hiển thị kết quả học tập qua biểu đồ tròn (phân bố xếp loại) và biểu đồ cột (điểm trung bình theo đề thi).
- **Kiến trúc MVC** : Giao diện đồ họa (GUI) thân thiện được tách biệt hoàn toàn với logic tính toán, sử dụng Pandas để quản lý cơ sở dữ liệu giúp dự án dễ dàng bảo trì và mở rộng.

## Cấu trúc Dự án
```text
EzGrade/
├── controllers/             # Chứa logic điều khiển (phối hợp giữa View và Model)
├── data/                    # Nơi lưu trữ database (exams.csv, students.csv)
├── models/                  # Chứa logic tính toán và xử lý dữ liệu (Pandas, Numpy)
├── utils/                   # Các tiện ích hỗ trợ
├── views/                   # Giao diện người dùng Tkinter hiện đại
├── venv/                    # Môi trường ảo chứa các thư viện phụ thuộc
├── main.py                  # File khởi chạy ứng dụng chính
├── requirements.txt         # Khai báo các thư viện Python phụ thuộc cần cài đặt
└── README.md                # Tài liệu hướng dẫn chính, tổng quan về dự án
```

## Hướng dẫn cài đặt và sử dụng dành cho Nhà phát triển

Để hệ thống hoạt động trơn tru từ khi sao chép về máy, hãy thực hiện theo các bước sau:

### 1. Khởi tạo môi trường
Bạn có thể thiết lập môi trường bằng các lệnh sau trên Terminal/Command Prompt:

- Tạo một môi trường ảo có tên là `venv`:
  ```bash
  python -m venv venv
  ```
- Kích hoạt môi trường:
  ```bash
  venv\Scripts\activate
  ```
- Cài đặt toàn bộ thư viện cần thiết từ `requirements.txt` (như pandas, numpy, matplotlib):
  ```bash
  pip install -r requirements.txt
  ```

### 2. Chạy ứng dụng
Sau khi thiết lập môi trường, bạn có thể chạy phần mềm bằng lệnh:

```bash
venv\Scripts\activate
python main.py
```

### 3. Đóng gói ra File Thực thi (.exe)
Để phân phối cho người dùng cuối cùng (không cần cài đặt Python), bạn có thể đóng gói ứng dụng bằng thư viện `PyInstaller`:
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile main.py
```
Hệ thống sẽ sử dụng PyInstaller để biên dịch toàn bộ tệp thành phần mã nguồn chạy độc lập trong thư mục `dist/`.

### 4. Dọn dẹp
Để lấy lại dung lượng bộ nhớ, bạn có thể xóa các thư mục `build`, `dist` và bộ đệm tệp của Python nếu không cần đóng gói ứng dụng nữa.

### 5. Cập nhật thư viện (Phụ thuộc)
Trong quá trình phát triển, nếu bạn cài đặt thêm các thư viện mới, hãy chạy lệnh sau trong thiết bị đầu cuối (đã kích hoạt môi trường ảo `venv`) để cập nhật lại tệp `requirements.txt`:
```bash
pip freeze > requirements.txt
```

## Tác giả / Người đóng góp
* **Trần Anh Tuấn**
* Chức vụ: Sinh Viên khoa cntt UHL (Trường Đại học Hạ Long)
* Email: dzcocs4@gmail.com

**Nhóm thực hiện:** Nhóm 2 - Lớp TT02A
Thành Viên :
1.Trần Anh Tuấn
2.Vũ Văn Duy Anh
3.Nguyên Đức Trung
4.Dịp Đức Phương