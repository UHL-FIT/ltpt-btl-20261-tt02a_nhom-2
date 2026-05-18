import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        self.setup_ui()
        
    def setup_ui(self):
        self.root.configure(bg="#F8F9FA")
        
        # Apply global styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Global frame and label backgrounds
        style.configure("TFrame", background="#F8F9FA")
        style.configure("TLabel", background="#F8F9FA", foreground="#333333", font=("Segoe UI", 10))
        
        # Dashboard specific styles
        style.configure("Dashboard.TFrame", background="#1A73E8")
        style.configure("DashTitle.TLabel", background="#1A73E8", foreground="#FFFFFF", font=("Segoe UI", 16, "bold"))
        
        # Card styles
        style.configure("Card.TFrame", background="#FFFFFF")
        style.configure("CardValue.TLabel", background="#FFFFFF", foreground="#1A73E8", font=("Segoe UI", 16, "bold"))
        style.configure("CardTitle.TLabel", background="#FFFFFF", foreground="#666666", font=("Segoe UI", 10, "bold"))
        
        # Button styles
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("Add.TButton", background="#34A853", foreground="#FFFFFF")
        style.configure("Edit.TButton", background="#FBBC04", foreground="#333333")
        style.configure("Delete.TButton", background="#EA4335", foreground="#FFFFFF")
        style.configure("Action.TButton", background="#e8f0fe", foreground="#1A73E8")
        
        # Treeview styles
        style.configure("Treeview", rowheight=25, font=("Segoe UI", 10), background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#E9ECEF", foreground="#333333")
        style.map('Treeview', background=[('selected', '#CCE5FF')], foreground=[('selected', '#004085')])

        # ---------------------------------------------------------
        # 1. Dashboard (Top Bar)
        # ---------------------------------------------------------
        dashboard_container = ttk.Frame(self.root, style="Dashboard.TFrame", padding=(15, 10))
        dashboard_container.pack(fill=tk.X)
        
        title_label = ttk.Label(dashboard_container, text="EZGRADE DASHBOARD", style="DashTitle.TLabel")
        title_label.pack(side=tk.TOP, pady=(0, 10))
        
        # Cards frame
        cards_frame = ttk.Frame(dashboard_container, style="Dashboard.TFrame")
        cards_frame.pack(side=tk.TOP, fill=tk.X)
        cards_frame.columnconfigure((0,1,2,3,4), weight=1)
        
        self.lbl_total = self._create_dashboard_card(cards_frame, 0, "👤 Tổng sinh viên", "0")
        self.lbl_avg = self._create_dashboard_card(cards_frame, 1, "⭐ Điểm TB", "0.0")
        self.lbl_pass = self._create_dashboard_card(cards_frame, 2, "✅ Đạt (>=5)", "0", value_color="#28a745")
        self.lbl_fail = self._create_dashboard_card(cards_frame, 3, "❌ Chưa đạt (<5)", "0", value_color="#dc3545")
        self.lbl_exams = self._create_dashboard_card(cards_frame, 4, "📝 Số đề thi", "0")

        # ---------------------------------------------------------
        # 2. Toolbar (Centered)
        # ---------------------------------------------------------
        toolbar_container = ttk.Frame(self.root, padding=(15, 10))
        toolbar_container.pack(fill=tk.X)
        
        toolbar_frame = ttk.Frame(toolbar_container)
        toolbar_frame.pack(anchor=tk.CENTER) # Center the toolbar
        
        ttk.Button(toolbar_frame, text="➕ Thêm Thí Sinh", style="Add.TButton", width=16, command=self.controller.add_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar_frame, text="✏️ Sửa Thí Sinh", style="Edit.TButton", width=16, command=self.controller.edit_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar_frame, text="🗑️ Xóa Thí Sinh", style="Delete.TButton", width=16, command=self.controller.delete_student).pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        ttk.Button(toolbar_frame, text="📂 Import Thí Sinh", style="Action.TButton", width=18, command=self.controller.import_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar_frame, text="💾 Export Thí Sinh", style="Action.TButton", width=18, command=self.controller.export_csv).pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        ttk.Button(toolbar_frame, text="📝 QL Đề Thi", style="Action.TButton", width=14, command=self.controller.manage_exams).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar_frame, text="📊 Thống kê", style="Action.TButton", width=12, command=self.controller.show_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar_frame, text="ℹ️ Thông tin", style="Action.TButton", width=12, command=self.controller.show_about).pack(side=tk.LEFT, padx=5)

        # ---------------------------------------------------------
        # 3. Search and Filters
        # ---------------------------------------------------------
        filter_frame = ttk.Frame(self.root, padding=(15, 5))
        filter_frame.pack(fill=tk.X)
        
        # Search Entry with placeholder behavior
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=40, font=("Segoe UI", 10))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        self.search_placeholder = "Nhập mã thí sinh hoặc tên..."
        self.search_entry.insert(0, self.search_placeholder)
        self.search_entry.config(foreground="gray")
        
        self.search_entry.bind("<FocusIn>", self._on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self._on_search_focus_out)
        self.search_var.trace("w", self._on_search_change)

        ttk.Label(filter_frame, text="Lọc đề thi:").pack(side=tk.LEFT, padx=(20, 5))
        self.exam_filter_var = tk.StringVar(value="Tất cả")
        self.exam_combo = ttk.Combobox(filter_frame, textvariable=self.exam_filter_var, state="readonly", width=15)
        self.exam_combo.pack(side=tk.LEFT, padx=5)
        self.exam_combo.bind("<<ComboboxSelected>>", lambda e: self.controller.filter_data())
        
        ttk.Button(filter_frame, text="Làm mới", command=self.controller.reset_filters).pack(side=tk.LEFT, padx=10)

        # ---------------------------------------------------------
        # 4. Table (Treeview)
        # ---------------------------------------------------------
        table_frame = ttk.Frame(self.root, padding=(15, 5))
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("stt", "student_id", "name", "gender", "class", "exam", "score", "correct", "wrong", "grade", "date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        # Config tags for scores AND alternating rows
        self.tree.tag_configure('evenrow', background='#FFFFFF')
        self.tree.tag_configure('oddrow', background='#F8F9FA')
        
        # Override foreground for specific score grades
        self.tree.tag_configure('good', foreground='#155724')
        self.tree.tag_configure('average', foreground='#856404')
        self.tree.tag_configure('bad', foreground='#721c24')

        headings = [
            ("stt", "STT", 50),
            ("student_id", "Mã TS", 100),
            ("name", "Họ Tên", 150),
            ("gender", "Giới Tính", 80),
            ("class", "Lớp", 100),
            ("exam", "Mã Đề", 80),
            ("score", "Điểm", 80),
            ("correct", "Số Câu Đúng", 100),
            ("wrong", "Số Câu Sai", 100),
            ("grade", "Xếp Loại", 100),
            ("date", "Ngày Thi", 150)
        ]
        
        for col, text, width in headings:
            self.tree.heading(col, text=text, command=lambda c=col: self.controller.sort_treeview(c))
            anchor = tk.CENTER if col in ['stt', 'student_id', 'gender', 'class', 'exam', 'score', 'correct', 'wrong', 'grade', 'date'] else tk.W
            self.tree.column(col, width=width, anchor=anchor, stretch=tk.YES if col == 'name' else tk.NO)

        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=scrollbar_x.set)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", lambda e: self.controller.edit_student())

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Sẵn sàng.")
        
        style.configure("Status.TLabel", background="#FFFFFF", foreground="#666666", font=("Segoe UI", 9))
        status_bar = ttk.Label(self.root, textvariable=self.status_var, anchor=tk.W, padding=(15, 5), style="Status.TLabel")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _create_dashboard_card(self, parent, col, title, initial_value, value_color="#1A73E8"):
        card = ttk.Frame(parent, style="Card.TFrame", padding=(10, 15))
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        
        lbl_title = ttk.Label(card, text=title, style="CardTitle.TLabel", anchor="center")
        lbl_title.pack(fill=tk.X)
        
        lbl_value = ttk.Label(card, text=initial_value, style="CardValue.TLabel", anchor="center")
        if value_color:
            lbl_value.configure(foreground=value_color)
        lbl_value.pack(fill=tk.X, pady=(5,0))
        
        return lbl_value
        
    def _on_search_focus_in(self, event):
        if self.search_entry.get() == self.search_placeholder:
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(foreground="#333333")

    def _on_search_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, self.search_placeholder)
            self.search_entry.config(foreground="gray")
            
    def _on_search_change(self, *args):
        val = self.search_var.get()
        if val != self.search_placeholder:
            self.controller.filter_data()
