<<<<<<< HEAD
import tkinter as tk
from tkinter import messagebox
from models.exam_model import ExamModel
from models.student_model import StudentModel
from models.stats_model import StatsModel
from controllers.main_controller import MainController
from views.main_window import MainWindow

def main():
    root = tk.Tk()
    root.title("EzGrade - Hệ Thống Chấm Điểm Trắc Nghiệm")
    root.geometry("1100x700")
    root.minsize(800, 600)

    try:
        exam_model = ExamModel()
        student_model = StudentModel(exam_model)
        stats_model = StatsModel(student_model)
        
        app = MainController(root, exam_model, student_model, stats_model)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Lỗi Khởi Động", f"Đã xảy ra lỗi khi khởi động ứng dụng:\n{str(e)}")

if __name__ == "__main__":
    main()
=======
"""
main.py
=======
Khởi chạy ứng dụng "SmartAttend".
Thiết kế theo mô hình MVC sử dụng modules (không dùng class).

Phase 1: Giao diện CLI (Command Line Interface)
Phase 2: Nâng cấp lên GUI (Tkinter) — chỉ thay View + Controller, giữ nguyên Model.
"""

import sys
from utils.logger import setup_logger

__version__ = "1.0.0"
logger = setup_logger("main")

# Ép console sử dụng UTF-8 khi chạy file .exe để tránh lỗi UnicodeEncodeError
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from controllers import gui_controller
from controllers import cli_controller

if __name__ == "__main__":
    logger.info(f"=== Khởi chạy SmartAttend v{__version__} (Chế độ mặc định) ===")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        logger.info("Chuyển sang giao diện dòng lệnh (CLI) qua tham số.")
        cli_controller.chay_ung_dung()
    else:
        logger.info("Khởi động giao diện đồ hoạ (GUI).")
        gui_controller.chay_ung_dung()
>>>>>>> 12b557d1f3e0a53ecd3a08e65497bcf931436c77
