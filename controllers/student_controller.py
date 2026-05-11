from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from views.student_window import StudentWindow

class StudentController:
    def __init__(self, parent_root, student_model, exam_model, refresh_callback, student_id=None):
        self.student_model = student_model
        self.exam_model = exam_model
        self.refresh_callback = refresh_callback
        self.student_id = student_id
        
        self.view = StudentWindow(parent_root, self, student_id)
        
        self.load_exams()
        if student_id:
            self.load_student_data()
            
    def load_exams(self):
        exams = self.exam_model.get_all_exams()
        self.view.combo_exam['values'] = [e['exam_id'] for e in exams]
        
    def on_exam_selected(self, event):
        exam_id = self.view.combo_exam.get()
        exam = self.exam_model.get_exam(exam_id)
        if exam:
            self.generate_answer_grid(int(exam['num_questions']))
            
    def generate_answer_grid(self, num):
        for widget in self.view.scrollable_frame.winfo_children():
            widget.destroy()
            
        self.view.combo_answers = []
        cols = 5
        for i in range(num):
            row = i // cols
            col = i % cols
            
            frame = ttk.Frame(self.view.scrollable_frame, padding=(5, 2), style="Primary.TFrame")
            frame.grid(row=row, column=col, sticky="w")
            
            ttk.Label(frame, text=f"Câu {i+1}:", background="#FFFFFF").pack(side=tk.LEFT)
            var = tk.StringVar(value="")
            cb = ttk.Combobox(frame, textvariable=var, values=["A", "B", "C", "D"], width=4, state="readonly", font=("Segoe UI", 10))
            cb.pack(side=tk.LEFT, padx=(5, 0))
            self.view.combo_answers.append(var)
            
    def load_student_data(self):
        students = self.student_model.get_all_students()
        student = next((s for s in students if s['student_id'] == self.student_id), None)
        if student:
            self.view.entry_id.insert(0, student['student_id'])
            self.view.entry_id.config(state="readonly")
            self.view.entry_name.insert(0, student['name'])
            self.view.combo_gender.set(student['gender'])
            self.view.entry_class.insert(0, student['class_name'])
            self.view.combo_exam.set(student['exam_id'])
            
            # Generate grid based on exam
            exam = self.exam_model.get_exam(student['exam_id'])
            if exam:
                self.generate_answer_grid(int(exam['num_questions']))
                
                answers = student['answers'].split(',')
                for i, ans in enumerate(answers):
                    if i < len(self.view.combo_answers):
                        self.view.combo_answers[i].set(ans.strip())
                        
    def apply_fast_input(self, event):
        text = self.view.entry_fast.get().upper().strip()
        if not text or "VD:" in text.upper(): return
        
        # Split by comma or simply take chars if they are A,B,C,D
        if ',' in text:
            ans_list = [a.strip() for a in text.split(',')]
        else:
            ans_list = list(text) # Assume format ABCDA...
            
        for i, ans in enumerate(ans_list):
            if i < len(self.view.combo_answers) and ans in ["A", "B", "C", "D"]:
                self.view.combo_answers[i].set(ans)
                
    def save_student(self):
        student_id = self.view.entry_id.get().strip()
        name = self.view.entry_name.get().strip()
        gender = self.view.combo_gender.get()
        class_name = self.view.entry_class.get().strip()
        exam_id = self.view.combo_exam.get()
        
        if not all([student_id, name, class_name, exam_id]):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return
            
        answers = [v.get() for v in self.view.combo_answers]
        if any(not a for a in answers):
            messagebox.showerror("Lỗi", "Vui lòng chọn đầy đủ đáp án cho bài làm")
            return
            
        answers_str = ",".join(answers)
        
        try:
            if self.view.entry_id.cget("state") == "readonly":
                self.student_model.update_student(student_id, name, gender, class_name, exam_id, answers_str)
                messagebox.showinfo("Thành công", "Cập nhật thí sinh thành công")
            else:
                self.student_model.add_student(student_id, name, gender, class_name, exam_id, answers_str)
                messagebox.showinfo("Thành công", "Thêm thí sinh thành công")
                
            self.refresh_callback()
            self.view.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
