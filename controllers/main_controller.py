from tkinter import messagebox, filedialog
import threading
from views.main_window import MainWindow

class MainController:
    def __init__(self, root, exam_model, student_model, stats_model):
        self.root = root
        self.exam_model = exam_model
        self.student_model = student_model
        self.stats_model = stats_model
        
        self.view = MainWindow(root, self)
        self.current_sort_col = "stt"
        self.current_sort_reverse = False
        
        self.load_exam_filters()
        self.refresh_table()

    def load_exam_filters(self):
        exams = self.exam_model.get_all_exams()
        exam_ids = ["Tất cả"] + [e['exam_id'] for e in exams]
        self.view.exam_combo['values'] = exam_ids
        if self.view.exam_filter_var.get() not in exam_ids:
            self.view.exam_filter_var.set("Tất cả")

    def refresh_table(self, data=None):
        if data is None:
            data = self.student_model.get_all_students()
            
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
            
        for i, row in enumerate(data, 1):
            values = (
                i,
                row['student_id'],
                row['name'],
                row['gender'],
                row['class_name'],
                row['exam_id'],
                row['score'],
                row['correct'],
                row['wrong'],
                row['grade'],
                row['date']
            )
            score = float(row.get('score', 0))
            grade_tag = 'good' if score >= 8.0 else ('average' if score >= 5.0 else 'bad')
            row_tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            
            self.view.tree.insert("", "end", values=values, tags=(row_tag, grade_tag))
            
        self.update_status()

    def update_status(self):
        stats = self.stats_model.get_summary_stats()
        exams_count = len(self.exam_model.get_all_exams())
        df = self.student_model.df
        pass_count = len(df[df['score'] >= 5.0]) if not df.empty else 0
        fail_count = len(df[df['score'] < 5.0]) if not df.empty else 0
        
        self.view.lbl_total.config(text=str(stats['total_students']))
        self.view.lbl_avg.config(text=str(stats['avg_score']))
        self.view.lbl_pass.config(text=str(pass_count))
        self.view.lbl_fail.config(text=str(fail_count))
        self.view.lbl_exams.config(text=str(exams_count))
        
        self.view.status_var.set("Sẵn sàng.")

    def filter_data(self):
        keyword = self.view.search_var.get()
        exam_filter = self.view.exam_filter_var.get()
        data = self.student_model.search_students(keyword, exam_filter)
        self.refresh_table(data)

    def reset_filters(self):
        self.view.search_var.set("")
        self.view.exam_filter_var.set("Tất cả")
        self.filter_data()

    def add_student(self):
        exams = self.exam_model.get_all_exams()
        if not exams:
            messagebox.showwarning("Cảnh báo", "Chưa có đề thi nào. Vui lòng tạo đề thi trước!")
            return
            
        from controllers.student_controller import StudentController
        StudentController(self.root, self.student_model, self.exam_model, self.refresh_table)

    def edit_student(self):
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Vui lòng chọn một thí sinh để sửa!")
            return
        
        item = self.view.tree.item(selected[0])
        student_id = item['values'][1]
        
        from controllers.student_controller import StudentController
        StudentController(self.root, self.student_model, self.exam_model, self.refresh_table, student_id)

    def delete_student(self):
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Vui lòng chọn một thí sinh để xóa!")
            return
            
        item = self.view.tree.item(selected[0])
        student_id = str(item['values'][1])
        name = item['values'][2]
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa thí sinh {name} (Mã: {student_id})?"):
            try:
                self.student_model.delete_student(student_id)
                self.refresh_table()
                messagebox.showinfo("Thành công", "Đã xóa thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def import_csv(self):
        filepath = filedialog.askopenfilename(
            title="Chọn file CSV thí sinh",
            filetypes=[("CSV files", "*.csv")]
        )
        if filepath:
            self.view.status_var.set("Đang import dữ liệu... Vui lòng chờ")
            self.root.update()
            
            def run_import():
                try:
                    result_msg = self.student_model.import_csv(filepath)
                    self.root.after(0, lambda: self.on_import_success(result_msg))
                except Exception as e:
                    self.root.after(0, lambda: self.on_import_error(str(e)))
                    
            threading.Thread(target=run_import, daemon=True).start()

    def on_import_success(self, msg):
        self.refresh_table()
        self.view.status_var.set("Sẵn sàng.")
        messagebox.showinfo("Import thành công", msg)
        
    def on_import_error(self, err_msg):
        self.view.status_var.set("Lỗi import.")
        messagebox.showerror("Lỗi Import", err_msg)

    def export_csv(self):
        filepath = filedialog.asksaveasfilename(
            title="Lưu file CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if filepath:
            try:
                self.student_model.export_csv(filepath)
                messagebox.showinfo("Thành công", "Export dữ liệu thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi Export", str(e))

    def manage_exams(self):
        from controllers.exam_controller import ExamController
        ExamController(self.root, self.exam_model, self.on_exam_changed)
        
    def on_exam_changed(self):
        self.load_exam_filters()
        self.filter_data() # Update current view based on current filters

    def show_stats(self):
        from views.stats_window import StatsWindow
        StatsWindow(self.root, self.stats_model)

    def show_about(self):
        about_text = (
            "EzGrade - Hệ Thống Chấm Điểm Trắc Nghiệm\n\n"
            "Phiên bản: 2.0.0\n"
            "Môn học: Lập trình Python\n"
            "Tác giả: Nhóm 2\n"
            "Ngày phát hành: Năm 2023\n\n"
            "Chức năng chính:\n"
            "- Quản lý danh sách thí sinh và đề thi\n"
            "- Tự động chấm điểm bằng NumPy array\n"
            "- Thống kê chi tiết, phân tích hiệu suất từng câu\n"
            "- Import/Export dữ liệu tối ưu với Pandas\n"
            "- Kiến trúc MVC hoàn chỉnh"
        )
        messagebox.showinfo("Thông tin phần mềm", about_text)

    def sort_treeview(self, col):
        # Basic sorting logic
        if self.current_sort_col == col:
            self.current_sort_reverse = not self.current_sort_reverse
        else:
            self.current_sort_reverse = False
            self.current_sort_col = col

        data = [(self.view.tree.set(child, col), child) for child in self.view.tree.get_children("")]
        
        # Try to convert to float for numeric sorting
        try:
            data.sort(key=lambda t: float(t[0]), reverse=self.current_sort_reverse)
        except ValueError:
            data.sort(key=lambda t: t[0].lower(), reverse=self.current_sort_reverse)

        for index, (_, child) in enumerate(data):
            self.view.tree.move(child, "", index)
            # Update STT column
            self.view.tree.set(child, "stt", index + 1)
