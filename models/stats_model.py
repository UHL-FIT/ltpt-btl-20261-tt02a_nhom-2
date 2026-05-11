import pandas as pd
import numpy as np

class StatsModel:
    def __init__(self, student_model):
        self.student_model = student_model

    def get_summary_stats(self):
        df = self.student_model.df
        if df.empty:
            return {
                "total_students": 0,
                "avg_score": 0.0,
                "max_score": 0.0,
                "min_score": 0.0,
                "pass_rate": 0.0
            }
        
        total = len(df)
        avg_score = round(df["score"].mean(), 2)
        max_score = df["score"].max()
        min_score = df["score"].min()
        pass_count = len(df[df["score"] >= 5.0])
        pass_rate = round((pass_count / total) * 100, 2) if total > 0 else 0

        return {
            "total_students": total,
            "avg_score": avg_score,
            "max_score": max_score,
            "min_score": min_score,
            "pass_rate": pass_rate
        }

    def get_grade_distribution(self):
        df = self.student_model.df
        if df.empty:
            return {}
        return df["grade"].value_counts().to_dict()
        
    def get_exam_performance(self):
        df = self.student_model.df
        if df.empty:
            return {}
        # Returns a dict grouping by exam_id the average score
        return df.groupby("exam_id")["score"].mean().round(2).to_dict()

    def get_question_analysis(self, exam_id):
        exam = self.student_model.exam_model.get_exam(exam_id)
        if not exam:
            return None
        
        students = self.student_model.df[self.student_model.df['exam_id'] == exam_id]
        if students.empty:
            return None
            
        correct_key = np.array([a.strip() for a in exam['answer_key'].split(',')])
        num_q = len(correct_key)
        
        student_answers = []
        for ans_str in students['answers']:
            ans_arr = np.array([a.strip() for a in str(ans_str).split(',')])
            if len(ans_arr) == num_q:
                student_answers.append(ans_arr)
            else:
                padded = np.zeros(num_q, dtype=str)
                m = min(len(ans_arr), num_q)
                padded[:m] = ans_arr[:m]
                student_answers.append(padded)
                
        if not student_answers:
            return None
            
        stu_mat = np.array(student_answers)
        correct_mat = (stu_mat == correct_key)
        correct_counts = np.sum(correct_mat, axis=0)
        total_students = len(student_answers)
        
        correct_rates = (correct_counts / total_students) * 100
        
        hardest_idx = np.argmin(correct_rates)
        easiest_idx = np.argmax(correct_rates)
        
        return {
            "rates": correct_rates.round(2).tolist(),
            "hardest_q": hardest_idx + 1,
            "hardest_rate": correct_rates[hardest_idx].round(2),
            "easiest_q": easiest_idx + 1,
            "easiest_rate": correct_rates[easiest_idx].round(2)
        }
