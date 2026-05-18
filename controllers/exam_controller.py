from tkinter import messagebox, filedialog
import tkinter as tk
import threading
from tkinter import ttk
from views.exam_window import ExamWindow
from utils.helpers import show_import_guide

class ExamController:
    def __init__(self, parent_root, exam_model, on_change_callback):
        self.exam_model = exam_model
        self.on_change_callback = on_change_callback
        self.view = ExamWindow(parent_root, self)
        self.refresh_table()
        
    def refresh_table(self):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
            
        exams = self.exam_model.get_all_exams()
        for e in exams:
            self.view.tree.insert("", "end", values=(e["exam_id"], e["exam_name"], e["num_questions"]))
            
    def on_select_exam(self, event):
        selected = self.view.tree.selection()
        if not selected:
            return
            
        item = self.view.tree.item(selected[0])
        exam_id = item['values'][0]
        
        exam = self.exam_model.get_exam(exam_id)
        if exam:
            self.view.entry_id.delete(0, tk.END)
            self.view.entry_id.insert(0, exam["exam_id"])
            self.view.entry_id.config(state="readonly")
            
            self.view.entry_name.delete(0, tk.END)
            self.view.entry_name.insert(0, exam["exam_name"])
            
            self.view.var_num_questions.set(exam["num_questions"])
            
            self.generate_answer_grid(int(exam["num_questions"]))
            
            # Fill answers
            answers = exam["answer_key"].split(",")
            for i, ans in enumerate(answers):
                if i < len(self.view.combo_answers):
                    self.view.combo_answers[i].set(ans.strip())

    def clear_form(self):
        self.view.tree.selection_remove(self.view.tree.selection())
        self.view.entry_id.config(state="normal")
        self.view.entry_id.delete(0, tk.END)
        self.view.entry_name.delete(0, tk.END)
        self.view.var_num_questions.set("10")
        
        # Clear grid
        for widget in self.view.scrollable_frame.winfo_children():
            widget.destroy()
        self.view.combo_answers = []
        
    def generate_answer_grid(self, num=None):
        if num is None:
            try:
                num = int(self.view.var_num_questions.get())
            except ValueError:
                messagebox.showerror("Lỗi", "Số câu hỏi phải là số nguyên", parent=self.view.window)
                self.view.window.lift()
                self.view.window.focus_force()
                self.view.entry_num.focus()
                return
                
        if num <= 0 or num > 200:
            messagebox.showerror("Lỗi", "Số câu hỏi phải từ 1 đến 200", parent=self.view.window)
            self.view.window.lift()
            self.view.window.focus_force()
            self.view.entry_num.focus()
            return
            
        # Clear old grid
        for widget in self.view.scrollable_frame.winfo_children():
            widget.destroy()
            
        self.view.combo_answers = []
        
        cols = 5 # 5 questions per row
        for i in range(num):
            row = i // cols
            col = i % cols
            
            frame = ttk.Frame(self.view.scrollable_frame, padding=(5, 2), style="Primary.TFrame")
            frame.grid(row=row, column=col, sticky="w")
            
            ttk.Label(frame, text=f"Câu {i+1}:", background="#FFFFFF").pack(side=tk.LEFT)
            var = tk.StringVar(value="A")
            cb = ttk.Combobox(frame, textvariable=var, values=["A", "B", "C", "D"], width=4, state="readonly", font=("Segoe UI", 10))
            cb.pack(side=tk.LEFT, padx=(5, 0))
            self.view.combo_answers.append(var)
            
    def save_exam(self):
        exam_id = self.view.entry_id.get().strip()
        exam_name = self.view.entry_name.get().strip()
        
        if not exam_id or not exam_name:
            messagebox.showerror("Lỗi", "Mã đề và Tên đề không được để trống", parent=self.view.window)
            self.view.window.lift()
            self.view.window.focus_force()
            if not exam_id: self.view.entry_id.focus()
            else: self.view.entry_name.focus()
            return
            
        try:
            num = int(self.view.var_num_questions.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Số câu hỏi không hợp lệ", parent=self.view.window)
            self.view.window.lift()
            self.view.window.focus_force()
            self.view.entry_num.focus()
            return
            
        if len(self.view.combo_answers) != num:
            messagebox.showerror("Lỗi", "Vui lòng bấm 'Tạo lưới đáp án' trước khi lưu", parent=self.view.window)
            self.view.window.lift()
            self.view.window.focus_force()
            self.view.entry_num.focus()
            return
            
        answers = [v.get() for v in self.view.combo_answers]
        if any(not a for a in answers):
            messagebox.showerror("Lỗi", "Vui lòng chọn đầy đủ đáp án", parent=self.view.window)
            self.view.window.lift()
            self.view.window.focus_force()
            if self.view.combo_answers: self.view.combo_answers[0].focus()
            return
            
        answer_key = ",".join(answers)
        
        try:
            # Check if updating or adding
            if self.view.entry_id.cget("state") == "readonly":
                self.exam_model.update_exam(exam_id, exam_name, num, answer_key)
                messagebox.showinfo("Thành công", "Cập nhật đề thi thành công", parent=self.view.window)
            else:
                self.exam_model.add_exam(exam_id, exam_name, num, answer_key)
                messagebox.showinfo("Thành công", "Thêm đề thi mới thành công", parent=self.view.window)
                
            self.refresh_table()
            self.on_change_callback()
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e), parent=self.view.window)
            self.view.window.lift()
            self.view.window.focus_force()
            
    def delete_exam(self):
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Vui lòng chọn đề thi để xóa", parent=self.view.window)
            self.view.window.lift()
            self.view.window.focus_force()
            return
            
        item = self.view.tree.item(selected[0])
        exam_id = str(item['values'][0])
        
        if messagebox.askyesno("Xác nhận", f"Xóa đề thi {exam_id}?"):
            try:
                self.exam_model.delete_exam(exam_id)
                self.refresh_table()
                self.on_change_callback()
                self.clear_form()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e), parent=self.view.window)
                self.view.window.lift()
                self.view.window.focus_force()
                
    def import_exams(self):
        cols_info = [
            ("exam_id", "Mã đề thi (Bắt buộc, không trùng lặp)"),
            ("exam_name", "Tên đề thi"),
            ("num_questions", "Số câu hỏi (Bắt buộc, phải là số nguyên > 0)"),
            ("answer_key", "Đáp án chuẩn (Bắt buộc, cách nhau bởi dấu phẩy, vd: A,B,C)")
        ]
        sample = "DE01,Đề thi giữa kỳ 1,10,\"A, B, C, D, A, B, C, D, A, B\""
        
        def on_accept():
            filepath = filedialog.askopenfilename(
                title="Chọn file CSV Đề Thi",
                filetypes=[("CSV files", "*.csv")]
            )
            if filepath:
                def run_import():
                    try:
                        msg = self.exam_model.import_csv(filepath)
                        self.view.window.after(0, lambda: self.on_import_success(msg))
                    except Exception as e:
                        self.view.window.after(0, lambda: self.on_import_error(str(e)))
                        
                threading.Thread(target=run_import, daemon=True).start()

        show_import_guide(self.view.window, "Hướng dẫn Import Đề Thi", cols_info, sample, on_accept)

    def on_import_success(self, msg):
        self.refresh_table()
        self.on_change_callback()
        messagebox.showinfo("Import Thành Công", msg, parent=self.view.window)
        
    def on_import_error(self, err_msg):
        messagebox.showerror("Lỗi Import", err_msg, parent=self.view.window)
        self.view.window.lift()
        self.view.window.focus_force()

    def export_exams(self):
        filepath = filedialog.asksaveasfilename(
            title="Lưu file CSV Đề Thi",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if filepath:
            try:
                self.exam_model.export_csv(filepath)
                messagebox.showinfo("Thành công", "Export dữ liệu thành công!", parent=self.view.window)
            except Exception as e:
                messagebox.showerror("Lỗi Export", str(e), parent=self.view.window)
                self.view.window.lift()
                self.view.window.focus_force()
