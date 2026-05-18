import tkinter as tk
from tkinter import ttk, messagebox

class ExamWindow:
    def __init__(self, parent, controller):
        self.window = tk.Toplevel(parent)
        self.window.title("Quản lý Đề Thi")
        self.window.geometry("800x600")
        self.window.grab_set() # Modal
        
        self.controller = controller
        
        self.setup_ui()
        
    def setup_ui(self):
        self.window.configure(bg="#F8F9FA")
        
        # Main layout container
        main_container = ttk.Frame(self.window, padding=15)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left Panel (Exam List)
        left_panel = ttk.LabelFrame(main_container, text="Danh sách đề thi", padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right Panel (Form)
        right_panel = ttk.LabelFrame(main_container, text="Thông tin đề thi", padding=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ---------------------------------------------------------
        # Left Panel content: Treeview and Actions
        # ---------------------------------------------------------
        table_frame = ttk.Frame(left_panel)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        columns = ("exam_id", "exam_name", "num_questions")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("exam_id", text="Mã Đề")
        self.tree.heading("exam_name", text="Tên Đề Thi")
        self.tree.heading("num_questions", text="Số Câu")
        
        self.tree.column("exam_id", width=80, anchor=tk.CENTER)
        self.tree.column("exam_name", width=150, anchor=tk.W)
        self.tree.column("num_questions", width=60, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.tree.bind("<<TreeviewSelect>>", self.controller.on_select_exam)
        
        # Actions in Left Panel
        action_frame = ttk.Frame(left_panel)
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="🗑️ Xóa", style="Delete.TButton", command=self.controller.delete_exam).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(action_frame, text="📂 Import CSV", style="Action.TButton", command=self.controller.import_exams).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="💾 Export CSV", style="Action.TButton", command=self.controller.export_exams).pack(side=tk.LEFT, padx=5)

        # ---------------------------------------------------------
        # Right Panel content: Form
        # ---------------------------------------------------------
        # Input Form Grid
        form_grid = ttk.Frame(right_panel)
        form_grid.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_grid, text="Mã đề:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.entry_id = ttk.Entry(form_grid, width=15, font=("Segoe UI", 10))
        self.entry_id.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_grid, text="Tên đề:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.entry_name = ttk.Entry(form_grid, width=30, font=("Segoe UI", 10))
        self.entry_name.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_grid, text="Số câu:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        num_frame = ttk.Frame(form_grid)
        num_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        self.var_num_questions = tk.StringVar(value="10")
        self.entry_num = ttk.Spinbox(num_frame, from_=1, to=200, width=5, textvariable=self.var_num_questions, font=("Segoe UI", 10))
        self.entry_num.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(num_frame, text="Tạo lưới đáp án", style="Action.TButton", command=self.controller.generate_answer_grid).pack(side=tk.LEFT)
        
        # Right Panel Bottom Actions (Packed first to stay at bottom)
        bottom_actions = ttk.Frame(right_panel)
        bottom_actions.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        ttk.Button(bottom_actions, text="🔄 Làm mới", style="Action.TButton", command=self.controller.clear_form).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(bottom_actions, text="💾 Lưu đề thi", style="Add.TButton", command=self.controller.save_exam).pack(side=tk.RIGHT)

        # Grid container (Scrollable Canvas)
        grid_container = ttk.LabelFrame(right_panel, text="Lưới đáp án", padding=5)
        grid_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(10, 10))
        
        self.canvas = tk.Canvas(grid_container, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar_ans = ttk.Scrollbar(grid_container, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas, style="Primary.TFrame")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_ans.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_ans.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.combo_answers = []
