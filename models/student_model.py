import pandas as pd
import numpy as np
import os
from datetime import datetime
from utils.constants import STUDENTS_FILE
from utils.helpers import ensure_dir, get_grade

class StudentModel:
    def __init__(self, exam_model):
        self.file_path = STUDENTS_FILE
        self.exam_model = exam_model
        ensure_dir("data")
        self._load_data()

    def _load_data(self):
        cols = ["student_id", "name", "gender", "class_name", "exam_id", "answers", 
                "score", "correct", "wrong", "grade", "date"]
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=cols)
            df.to_csv(self.file_path, index=False, encoding='utf-8')
        try:
            self.df = pd.read_csv(self.file_path, dtype={"student_id": str, "exam_id": str})
        except Exception:
            self.df = pd.DataFrame(columns=cols)

    def _save_data(self):
        self.df.to_csv(self.file_path, index=False, encoding='utf-8')

    def get_all_students(self):
        return self.df.to_dict('records')
        
    def search_students(self, keyword, exam_filter="Tất cả"):
        df = self.df
        if exam_filter != "Tất cả":
            df = df[df["exam_id"] == exam_filter]
            
        if not keyword:
            return df.to_dict('records')
            
        keyword = keyword.lower()
        mask = (
            df['student_id'].astype(str).str.lower().str.contains(keyword) |
            df['name'].astype(str).str.lower().str.contains(keyword) |
            df['class_name'].astype(str).str.lower().str.contains(keyword)
        )
        return df[mask].to_dict('records')

    def calculate_score(self, exam_id, student_answers_str):
        exam = self.exam_model.get_exam(exam_id)
        if not exam:
            raise ValueError("Đề thi không tồn tại.")
        
        correct_answers_str = exam['answer_key']
        cor_arr = np.array([ans.strip().upper() for ans in correct_answers_str.split(',') if ans.strip()])
        stu_arr = np.array([ans.strip().upper() for ans in str(student_answers_str).split(',') if ans.strip()])
        
        valid_ans = {"A", "B", "C", "D"}
        if not all(a in valid_ans for a in stu_arr):
            raise ValueError("Đáp án chứa ký tự không hợp lệ (Chỉ cho phép A, B, C, D).")
            
        if len(cor_arr) != len(stu_arr):
            raise ValueError(f"Số lượng câu trả lời ({len(stu_arr)}) không khớp với đề thi ({len(cor_arr)}).")
        
        correct_count = np.sum(cor_arr == stu_arr)
        total = len(cor_arr)
        wrong_count = total - correct_count
        score = round((correct_count / total) * 10, 2) if total > 0 else 0
        grade = get_grade(score)
        
        return correct_count, wrong_count, score, grade

    def add_student(self, student_id, name, gender, class_name, exam_id, answers_str):
        if student_id in self.df["student_id"].values:
            raise ValueError(f"Mã thí sinh '{student_id}' đã tồn tại.")
            
        correct, wrong, score, grade = self.calculate_score(exam_id, answers_str)
        
        new_row = {
            "student_id": student_id,
            "name": name,
            "gender": gender,
            "class_name": class_name,
            "exam_id": exam_id,
            "answers": answers_str,
            "score": score,
            "correct": correct,
            "wrong": wrong,
            "grade": grade,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self._save_data()

    def update_student(self, student_id, name, gender, class_name, exam_id, answers_str):
        idx = self.df.index[self.df["student_id"] == student_id].tolist()
        if not idx:
            raise ValueError(f"Mã thí sinh '{student_id}' không tồn tại.")
            
        correct, wrong, score, grade = self.calculate_score(exam_id, answers_str)
        
        i = idx[0]
        self.df.at[i, "name"] = name
        self.df.at[i, "gender"] = gender
        self.df.at[i, "class_name"] = class_name
        self.df.at[i, "exam_id"] = exam_id
        self.df.at[i, "answers"] = answers_str
        self.df.at[i, "score"] = score
        self.df.at[i, "correct"] = correct
        self.df.at[i, "wrong"] = wrong
        self.df.at[i, "grade"] = grade
        self._save_data()

    def delete_student(self, student_id):
        if student_id not in self.df["student_id"].values:
            raise ValueError(f"Mã thí sinh '{student_id}' không tồn tại.")
        self.df = self.df[self.df["student_id"] != student_id]
        self._save_data()
        
    def import_csv(self, filepath):
        try:
            if os.path.getsize(filepath) == 0:
                raise ValueError("File CSV rỗng.")
                
            new_df = pd.read_csv(filepath, dtype={"student_id": str, "exam_id": str})
            if new_df.empty:
                raise ValueError("File CSV không có dữ liệu.")
                
            required_cols = {"student_id", "name", "gender", "class_name", "exam_id", "answers"}
            if not required_cols.issubset(new_df.columns):
                raise ValueError(f"File CSV cần các cột: {', '.join(required_cols)}")
            
            records = new_df.to_dict('records')
            valid_records = []
            errors = []
            
            for i, row in enumerate(records):
                try:
                    if pd.isna(row['student_id']) or pd.isna(row['exam_id']) or pd.isna(row['answers']):
                        raise ValueError("Thiếu dữ liệu bắt buộc (ID, Exam, Answers).")
                        
                    c, w, s, g = self.calculate_score(row['exam_id'], row['answers'])
                    row['score'] = s
                    row['correct'] = c
                    row['wrong'] = w
                    row['grade'] = g
                    row['date'] = row.get('date', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    if pd.isna(row['date']):
                        row['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    valid_records.append(row)
                except Exception as e:
                    errors.append(f"Dòng {i+2} (Mã TS: {row.get('student_id', 'N/A')}): {str(e)}")

            if not valid_records:
                err_msg = "\n".join(errors[:5]) + ("\n..." if len(errors) > 5 else "")
                raise ValueError(f"Không có dữ liệu hợp lệ để import. Chi tiết lỗi:\n{err_msg}")

            processed_df = pd.DataFrame(valid_records)
            
            # Check duplicate ID within the CSV
            if processed_df['student_id'].duplicated().any():
                raise ValueError("File CSV chứa các student_id trùng lặp nhau.")
                
            self.df = pd.concat([self.df, processed_df]).drop_duplicates(subset=['student_id'], keep='last').reset_index(drop=True)
            self._save_data()
            
            if errors:
                return f"Import thành công {len(valid_records)} dòng. Lỗi {len(errors)} dòng."
            return f"Import thành công toàn bộ {len(valid_records)} dòng."
            
        except pd.errors.EmptyDataError:
            raise ValueError("File CSV rỗng hoặc định dạng không đọc được.")
        except Exception as e:
            raise ValueError(f"Lỗi khi import thí sinh: {str(e)}")

    def export_csv(self, filepath):
        self.df.to_csv(filepath, index=False, encoding='utf-8-sig')
