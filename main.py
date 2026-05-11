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
