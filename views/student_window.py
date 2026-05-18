import tkinter as tk
from tkinter import ttk

class StudentWindow:
    def __init__(self, parent, controller, student_id=None):
        self.window = tk.Toplevel(parent)
        self.window.title("Thông tin Thí Sinh" if not student_id else f"Sửa Thí Sinh: {student_id}")
        self.window.geometry("700x500")
        self.window.grab_set()
        
        self.controller = controller
        self.setup_ui()
        
    def setup_ui(self):
        self.window.configure(bg="#F8F9FA")
        main_container = ttk.Frame(self.window, padding=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Info Frame
        info_frame = ttk.LabelFrame(main_container, text="Thông tin chung", padding=15)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Row 0
        ttk.Label(info_frame, text="Mã TS:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=10, padx=(0, 10))
        self.entry_id = ttk.Entry(info_frame, width=25, font=("Segoe UI", 10))
        self.entry_id.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(info_frame, text="Họ tên:", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky=tk.W, padx=(30, 10), pady=10)
        self.entry_name = ttk.Entry(info_frame, width=35, font=("Segoe UI", 10))
        self.entry_name.grid(row=0, column=3, sticky=tk.W, pady=10)
        
        # Row 1
        ttk.Label(info_frame, text="Giới tính:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=10, padx=(0, 10))
        self.combo_gender = ttk.Combobox(info_frame, values=["Nam", "Nữ", "Khác"], state="readonly", width=22, font=("Segoe UI", 10))
        self.combo_gender.grid(row=1, column=1, sticky=tk.W, pady=10)
        self.combo_gender.set("Nam")
        
        ttk.Label(info_frame, text="Lớp:", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, sticky=tk.W, padx=(30, 10), pady=10)
        self.entry_class = ttk.Entry(info_frame, width=35, font=("Segoe UI", 10))
        self.entry_class.grid(row=1, column=3, sticky=tk.W, pady=10)
        
        # Row 2
        ttk.Label(info_frame, text="Đề thi:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=10, padx=(0, 10))
        self.combo_exam = ttk.Combobox(info_frame, state="readonly", width=22, font=("Segoe UI", 10))
        self.combo_exam.grid(row=2, column=1, sticky=tk.W, pady=10)
        self.combo_exam.bind("<<ComboboxSelected>>", self.controller.on_exam_selected)
        
        # Fast input
        ttk.Label(info_frame, text="Nhập nhanh:", font=("Segoe UI", 10, "bold")).grid(row=2, column=2, sticky=tk.W, padx=(30, 10), pady=10)
        self.entry_fast = ttk.Entry(info_frame, width=35, font=("Segoe UI", 10))
        self.entry_fast.grid(row=2, column=3, sticky=tk.W, pady=10)
        self.entry_fast.insert(0, "Vd: A,B,C...")
        self.entry_fast.bind("<FocusIn>", lambda e: self._on_fast_input_focus())
        self.entry_fast.bind("<Return>", self.controller.apply_fast_input)
        
        # Action (Packed first to always stay at bottom)
        btn_frame = ttk.Frame(main_container)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Button(btn_frame, text="💾 Lưu Thí Sinh", style="Add.TButton", width=20, command=self.controller.save_student).pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text="📂 Import CSV", style="Action.TButton", width=20, command=self.controller.import_csv).pack(side=tk.LEFT)

        # Answer Frame
        ans_frame = ttk.LabelFrame(main_container, text="Bài làm", padding=10)
        ans_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.canvas = tk.Canvas(ans_frame, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(ans_frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas, style="Primary.TFrame")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.combo_answers = []

    def _on_fast_input_focus(self):
        if self.entry_fast.get() == "Vd: A,B,C...":
            self.entry_fast.delete(0, tk.END)
