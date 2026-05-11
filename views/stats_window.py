import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StatsWindow:
    def __init__(self, parent, stats_model):
        self.window = tk.Toplevel(parent)
        self.window.title("Thống kê & Phân tích")
        self.window.geometry("900x700")
        
        self.stats_model = stats_model
        self.setup_ui()
        
    def setup_ui(self):
        # Summary Frame
        summary_frame = tk.LabelFrame(self.window, text="Tổng quan", padx=10, pady=10)
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        stats = self.stats_model.get_summary_stats()
        
        ttk.Label(summary_frame, text=f"Tổng số thí sinh: {stats['total_students']}", font=('Segoe UI', 12, 'bold')).grid(row=0, column=0, padx=20, pady=5)
        ttk.Label(summary_frame, text=f"Điểm TB: {stats['avg_score']}", font=('Segoe UI', 12, 'bold')).grid(row=0, column=1, padx=20, pady=5)
        ttk.Label(summary_frame, text=f"Điểm cao nhất: {stats['max_score']}", font=('Segoe UI', 12, 'bold')).grid(row=0, column=2, padx=20, pady=5)
        ttk.Label(summary_frame, text=f"Tỷ lệ đạt (>=5.0): {stats['pass_rate']}%", font=('Segoe UI', 12, 'bold')).grid(row=0, column=3, padx=20, pady=5)
        
        # Per-Question Analysis Frame
        qa_frame = tk.LabelFrame(self.window, text="Phân tích hiệu suất câu hỏi (NumPy Vectorized)", padx=10, pady=10)
        qa_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(qa_frame, text="Chọn đề thi:").pack(side=tk.LEFT, padx=5)
        self.exam_var = tk.StringVar()
        
        exams = self.stats_model.student_model.exam_model.get_all_exams()
        exam_ids = [e['exam_id'] for e in exams]
        
        self.combo_exam = ttk.Combobox(qa_frame, textvariable=self.exam_var, values=exam_ids, state="readonly")
        self.combo_exam.pack(side=tk.LEFT, padx=5)
        self.combo_exam.bind("<<ComboboxSelected>>", self.update_question_analysis)
        
        self.lbl_qa_result = tk.Label(qa_frame, text="Vui lòng chọn đề thi để xem phân tích.", font=('Segoe UI', 10), fg="#0056b3")
        self.lbl_qa_result.pack(side=tk.LEFT, padx=20)
        
        # Charts Frame
        charts_frame = tk.Frame(self.window)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        
        self.draw_pie_chart()
        self.draw_bar_chart()
        
        self.fig.tight_layout()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=charts_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def draw_pie_chart(self):
        dist = self.stats_model.get_grade_distribution()
        if not dist:
            self.ax1.text(0.5, 0.5, 'Chưa có dữ liệu', ha='center', va='center')
            self.ax1.set_title('Phân bố Xếp loại')
            return
            
        labels = list(dist.keys())
        sizes = list(dist.values())
        colors = ['#28a745', '#17a2b8', '#ffc107', '#fd7e14', '#dc3545']
        
        self.ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors[:len(labels)])
        self.ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        self.ax1.set_title('Phân bố Xếp loại')
        
    def draw_bar_chart(self):
        perf = self.stats_model.get_exam_performance()
        if not perf:
            self.ax2.text(0.5, 0.5, 'Chưa có dữ liệu', ha='center', va='center')
            self.ax2.set_title('Điểm TB theo Đề thi')
            return
            
        exams = list(perf.keys())
        scores = list(perf.values())
        
        self.ax2.bar(exams, scores, color='#0056b3')
        self.ax2.set_ylim(0, 10)
        self.ax2.set_ylabel('Điểm TB')
        self.ax2.set_title('Điểm TB theo Đề thi')
        
        # Add values on top of bars
        for i, v in enumerate(scores):
            self.ax2.text(i, v + 0.1, str(v), ha='center')

    def update_question_analysis(self, event=None):
        exam_id = self.exam_var.get()
        if not exam_id:
            return
            
        qa = self.stats_model.get_question_analysis(exam_id)
        if not qa:
            self.lbl_qa_result.config(text="Chưa có đủ dữ liệu bài làm cho đề thi này.", fg="#dc3545")
            return
            
        result_text = (
            f"Câu khó nhất: Câu {qa['hardest_q']} ({qa['hardest_rate']}% đúng) | "
            f"Câu dễ nhất: Câu {qa['easiest_q']} ({qa['easiest_rate']}% đúng)\n"
            f"Tỷ lệ đúng từng câu: {qa['rates']}"
        )
        self.lbl_qa_result.config(text=result_text, fg="#28a745")
