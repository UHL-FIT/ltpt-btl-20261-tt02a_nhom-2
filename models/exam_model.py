import pandas as pd
import os
from utils.constants import EXAMS_FILE
from utils.helpers import ensure_dir

class ExamModel:
    def __init__(self):
        self.file_path = EXAMS_FILE
        ensure_dir("data")
        self._load_data()

    def _load_data(self):
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=["exam_id", "exam_name", "num_questions", "answer_key"])
            df.to_csv(self.file_path, index=False, encoding='utf-8')
        try:
            self.df = pd.read_csv(self.file_path, dtype={"exam_id": str})
        except Exception:
            self.df = pd.DataFrame(columns=["exam_id", "exam_name", "num_questions", "answer_key"])

    def _save_data(self):
        self.df.to_csv(self.file_path, index=False, encoding='utf-8')

    def get_all_exams(self):
        return self.df.to_dict('records')

    def get_exam(self, exam_id):
        exam = self.df[self.df["exam_id"] == exam_id]
        if not exam.empty:
            return exam.iloc[0].to_dict()
        return None

    def add_exam(self, exam_id, exam_name, num_questions, answer_key):
        if exam_id in self.df["exam_id"].values:
            raise ValueError(f"Mã đề thi '{exam_id}' đã tồn tại.")
        
        new_row = {
            "exam_id": exam_id,
            "exam_name": exam_name,
            "num_questions": int(num_questions),
            "answer_key": answer_key
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self._save_data()

    def update_exam(self, exam_id, exam_name, num_questions, answer_key):
        idx = self.df.index[self.df["exam_id"] == exam_id].tolist()
        if not idx:
            raise ValueError(f"Mã đề thi '{exam_id}' không tồn tại.")
        
        self.df.at[idx[0], "exam_name"] = exam_name
        self.df.at[idx[0], "num_questions"] = int(num_questions)
        self.df.at[idx[0], "answer_key"] = answer_key
        self._save_data()

    def delete_exam(self, exam_id):
        if exam_id not in self.df["exam_id"].values:
            raise ValueError(f"Mã đề thi '{exam_id}' không tồn tại.")
        self.df = self.df[self.df["exam_id"] != exam_id]
        self._save_data()
        
    def import_csv(self, filepath):
        try:
            if os.path.getsize(filepath) == 0:
                raise ValueError("File CSV rỗng.")
                
            try:
                new_df = pd.read_csv(filepath, dtype={"exam_id": str})
            except Exception:
                raise ValueError("Không thể đọc file CSV. Vui lòng kiểm tra lại định dạng file (phải là UTF-8, dấu phẩy ngăn cách).")

            if new_df.empty:
                raise ValueError("File CSV không có dòng dữ liệu nào.")
                
            required_cols = {"exam_id", "exam_name", "num_questions", "answer_key"}
            missing_cols = required_cols - set(new_df.columns)
            if missing_cols:
                raise ValueError(f"File CSV bị thiếu các cột bắt buộc: {', '.join(missing_cols)}")
            
            records = new_df.to_dict('records')
            valid_records = []
            errors = []
            
            for i, row in enumerate(records):
                try:
                    if pd.isna(row['exam_id']) or not str(row['exam_id']).strip():
                        raise ValueError("Thiếu Mã đề thi (exam_id).")
                    if pd.isna(row['num_questions']):
                        raise ValueError("Thiếu Số câu hỏi (num_questions).")
                    if pd.isna(row['answer_key']) or not str(row['answer_key']).strip():
                        raise ValueError("Thiếu Đáp án chuẩn (answer_key).")
                    
                    try:
                        num = int(row['num_questions'])
                        if num <= 0:
                            raise ValueError()
                    except ValueError:
                        raise ValueError(f"Số câu hỏi '{row['num_questions']}' không hợp lệ (phải là số nguyên > 0).")

                    ans = str(row['answer_key']).upper().split(',')
                    ans = [a.strip() for a in ans if a.strip()]
                    
                    if len(ans) != num:
                        raise ValueError(f"Số đáp án ({len(ans)}) không khớp số lượng câu hỏi ({num}).")
                        
                    valid_ans = {"A", "B", "C", "D"}
                    if not all(a in valid_ans for a in ans):
                        raise ValueError("Đáp án chứa ký tự không hợp lệ (Chỉ chấp nhận A, B, C, D).")
                        
                    row['answer_key'] = ",".join(ans)
                    valid_records.append(row)
                except Exception as e:
                    errors.append(f"- Dòng {i+2} (Mã đề: {row.get('exam_id', 'N/A')}): {str(e)}")
                    
            if not valid_records:
                err_msg = "\n".join(errors[:10]) + ("\n..." if len(errors) > 10 else "")
                raise ValueError(f"Không có dữ liệu hợp lệ để import. Chi tiết lỗi:\n{err_msg}")
                
            processed_df = pd.DataFrame(valid_records)

            # Check duplicate exam ID within CSV
            duplicates = processed_df[processed_df.duplicated(['exam_id'], keep=False)]
            if not duplicates.empty:
                dup_ids = duplicates['exam_id'].unique()
                raise ValueError(f"File CSV chứa các mã đề thi trùng lặp: {', '.join(dup_ids)}")
                
            self.df = pd.concat([self.df, processed_df]).drop_duplicates(subset=['exam_id'], keep='last').reset_index(drop=True)
            self._save_data()
            
            if errors:
                err_msg = "\n".join(errors[:5]) + ("\n..." if len(errors) > 5 else "")
                return f"Import thành công {len(valid_records)} đề thi.\n\nBỏ qua {len(errors)} đề thi bị lỗi:\n{err_msg}"
            return f"Import thành công toàn bộ {len(valid_records)} đề thi."
            
        except pd.errors.EmptyDataError:
            raise ValueError("File CSV rỗng hoặc định dạng không đọc được.")
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"Lỗi hệ thống khi import đề thi: {str(e)}")

    def export_csv(self, filepath):
        self.df.to_csv(filepath, index=False, encoding='utf-8-sig')
