# utils/helpers.py
import os

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_grade(score):
    from utils.constants import GRADE_SCALE
    for threshold, grade in GRADE_SCALE:
        if score >= threshold:
            return grade
    return "Yếu"
