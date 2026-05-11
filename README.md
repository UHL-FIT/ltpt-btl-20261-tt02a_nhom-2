<<<<<<< HEAD
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
=======
[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/-QmD8cHQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23820619&assignment_repo_type=AssignmentRepo)
# SmartAttend - Phần Mềm Quản Lý Điểm Danh Sinh Viên

SmartAttend là một ứng dụng Python chuyên dụng giúp giảng viên/người dùng quản lý thông tin sinh viên, điểm danh theo tuần, theo dõi số lần nộp bài tập, vi phạm và đưa ra các cảnh báo cấm thi một cách trực quan, hiện đại.

> **Lưu ý quan trọng**: Đây là dự án ví dụ cốt lõi (baseline) dành cho sinh viên tham khảo trong quá trình phát triển và hoàn thiện Bài tập lớn môn Lập trình Python. Mọi tính năng cơ bản của một ứng dụng quản lý đều được triển khai theo đúng chuẩn.
## Tính năng nổi bật
1. **Giao diện 2 trong 1**: Hỗ trợ cả giao diện đồ hoạ (GUI) trực quan thân thiện và giao diện dòng lệnh (CLI) nhẹ nhàng.
2. **Quản lý Sinh viên**: Thêm, Sửa, Xoá, và Tìm kiếm linh hoạt với bộ lọc (Tất cả, MSV, Họ tên, Giới tính, SĐT).
3. **Điểm danh Nhanh**: Tự động tính toán điểm chuyên cần theo từng lần điểm danh:
   - `M`: Có mặt
   - `P`: Vắng có phép (🟢)
   - `K`: Vắng không phép (🟥) - Bị trừ điểm.
4. **Cảnh báo Tự động**: Tự động dán nhãn màu "Cẩn thận cấm thi" (Cam) và "Cấm thi" (Đỏ) dựa trên số buổi vắng.
5. **Import/Export Dữ liệu**: Hỗ trợ nhập và xuất hàng loạt dữ liệu thông qua file `.csv`.

## Cấu trúc Dự án
```
ltpt_example/
├── assets/                  # Icon và tài nguyên ảnh
├── controllers/             # Chứa logic điều khiển (gui_controller.py, cli_controller.py)
├── data/                    # Nơi lưu trữ database (diemdanh.csv)
├── models/                  # Chứa logic tính toán và xử lý dữ liệu (diemdanh.py)
├── templates/               # Form mẫu CSV (diemdanh_template.csv) để import
├── utils/                   # Các tiện ích (Logger)
├── views/                   # Giao diện người dùng (gui_view.py, cli_view.py)
├── main.py                  # File khởi chạy ứng dụng chính
├── requirements.txt         # Khai báo các thư viện Python phụ thuộc cần cài đặt
├── README.md                # Tài liệu hướng dẫn chính, tổng quan về dự án
├── CONVENTIONS.md           # Tài liệu quy chuẩn viết code, commit và cấu trúc nhánh
├── SRS.md                   # Tài liệu Đặc tả Yêu cầu Hệ thống (Software Requirements Specification)
├── SAD.md                   # Tài liệu Thiết kế Kiến trúc Phần mềm (Software Architecture Document)
├── build.bat                # Script tự động đóng gói ứng dụng Python thành file thực thi (.exe)
├── clean.bat                # Script tự động dọn dẹp môi trường, xóa file rác, file tạm sau khi build
├── run_tests.bat            # Script tự động chạy toàn bộ các Unit Test của ứng dụng
└── setup_env.bat            # Script tự động tạo môi trường ảo (.venv) và cài đặt các thư viện cần thiết
```

## Hướng dẫn cài đặt và sử dụng dành cho Developer

### Thứ tự chạy các file Script (.bat)
Để hệ thống hoạt động trơn tru từ khi clone về máy, hãy chạy theo thứ tự sau:
1. Chạy **`setup_env.bat`**: Để tạo môi trường và tải thư viện.
2. Chạy **`main.py`** (thông qua lệnh python): Để chạy ứng dụng chính.
3. Chạy **`run_tests.bat`** (Tuỳ chọn): Để kiểm tra xem code có vượt qua các test cases không.
4. Chạy **`build.bat`** (Tuỳ chọn): Để xuất ra file `.exe` đem đi phân phối cho người dùng khác.
5. Chạy **`clean.bat`** (Tuỳ chọn): Dọn dẹp không gian đĩa nếu không cần thư mục build/dist nữa.

### 1. Khởi tạo môi trường
Bạn chỉ cần nhấp đúp chuột vào file `setup_env.bat` (trên Windows). 
Script này sẽ tự động:
- Tạo một môi trường ảo có tên là `.venv`.
- Kích hoạt môi trường ảo.
- Cài đặt toàn bộ thư viện cần thiết từ `requirements.txt` (như `pandas`, `numpy`, `pyinstaller`).

### 2. Chạy ứng dụng
Sau khi đã thiết lập môi trường, bạn có thể chạy phần mềm bằng lệnh:

**Chạy với Giao diện Đồ họa (GUI - Mặc định)**
```bash
.venv\Scripts\activate
python main.py
```

**Chạy với Giao diện Dòng lệnh (CLI - Terminal)**
Nếu bạn muốn sử dụng phần mềm trực tiếp trên môi trường dòng lệnh siêu nhẹ, hãy truyền thêm tham số `--cli`:
```bash
.venv\Scripts\activate
python main.py --cli
```

### 3. Đóng gói ra File Thực thi (.exe)
Để phân phối cho người dùng cuối (không cần cài đặt Python), hãy click đúp chuột vào file `build.bat`. 
Hệ thống sẽ dùng `PyInstaller` để biên dịch toàn bộ source code thành file `Setup_SmartAttend.exe` (Nếu bạn dùng thêm Inno Setup) hoặc bộ chạy độc lập trong thư mục `dist/`.

### 4. Dọn dẹp
Để lấy lại dung lượng bộ nhớ, bạn có thể chạy `clean.bat`. File này sẽ xóa các thư mục `build`, `dist` và các file cache của Python.

### 5. Cập nhật thư viện (Dependencies)
Trong quá trình phát triển, nếu bạn cài đặt thêm các thư viện mới, hãy chạy lệnh sau trong terminal (đã kích hoạt môi trường ảo `.venv`) để cập nhật lại file `requirements.txt`:
>>>>>>> 12b557d1f3e0a53ecd3a08e65497bcf931436c77
```bash
pip freeze > requirements.txt
```

<<<<<<< HEAD
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
=======
## Tác giả / Contributors
* **VŨ DUY SƠN**
* Chức vụ: Giảng viên UHL (Trường Đại học Hạ Long)
* Email: vuduyson@daihochalong.edu.vn / sonduyvu@gmail.com
>>>>>>> 12b557d1f3e0a53ecd3a08e65497bcf931436c77
