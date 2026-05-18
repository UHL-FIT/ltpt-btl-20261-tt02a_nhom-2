# utils/helpers.py
import os
import tkinter as tk
from tkinter import ttk

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_grade(score):
    from utils.constants import GRADE_SCALE
    for threshold, grade in GRADE_SCALE:
        if score >= threshold:
            return grade
    return "Yếu"

def show_import_guide(parent, title, columns_info, sample_data, on_accept):
    """
    Hiển thị popup hướng dẫn định dạng CSV trước khi import.
    - columns_info: list of tuples (Tên cột, Mô tả)
    - sample_data: string ví dụ một dòng CSV hợp lệ
    - on_accept: callback function được gọi khi người dùng bấm "Tiếp tục"
    """
    guide_win = tk.Toplevel(parent)
    guide_win.title(title)
    guide_win.geometry("650x550")
    guide_win.grab_set()
    guide_win.configure(bg="#F8F9FA")

    main_frame = ttk.Frame(guide_win, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Tiêu đề
    ttk.Label(main_frame, text="Hướng Dẫn Định Dạng File CSV", font=("Segoe UI", 14, "bold"), foreground="#1A73E8").pack(anchor=tk.W, pady=(0, 15))

    # Cột yêu cầu
    cols_frame = ttk.LabelFrame(main_frame, text="Các cột bắt buộc (theo đúng thứ tự)", padding=10)
    cols_frame.pack(fill=tk.X, pady=(0, 15))

    for col_name, desc in columns_info:
        row = ttk.Frame(cols_frame)
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text=col_name, font=("Segoe UI", 10, "bold"), width=15).pack(side=tk.LEFT)
        ttk.Label(row, text=f": {desc}", font=("Segoe UI", 10)).pack(side=tk.LEFT)

    # Ví dụ mẫu
    sample_frame = ttk.LabelFrame(main_frame, text="Ví dụ 1 dòng dữ liệu hợp lệ", padding=10)
    sample_frame.pack(fill=tk.X, pady=(0, 15))
    
    text_sample = tk.Text(sample_frame, height=3, font=("Consolas", 10), bg="#E9ECEF", relief="flat")
    text_sample.pack(fill=tk.X)
    
    headers = ",".join([col[0] for col in columns_info])
    text_sample.insert("1.0", f"{headers}\n{sample_data}")
    text_sample.config(state="disabled")

    # Lưu ý
    note_text = "Lưu ý: Không bỏ trống các trường dữ liệu quan trọng. Tránh ký tự đặc biệt."
    ttk.Label(main_frame, text=note_text, foreground="#D93025", font=("Segoe UI", 9, "italic")).pack(anchor=tk.W, pady=(0, 15))

    # Nút bấm
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    def accept():
        guide_win.destroy()
        on_accept()

    ttk.Button(btn_frame, text="Hủy bỏ", command=guide_win.destroy).pack(side=tk.RIGHT, padx=(10, 0))
    ttk.Button(btn_frame, text="Đã hiểu, chọn file...", style="Add.TButton", command=accept).pack(side=tk.RIGHT)
