from .db import get_db
from pymongo.errors import PyMongoError
from .models import GradeSubmission

class GradeService:

    @staticmethod
    def submit_grade(grade_submission: GradeSubmission):
        """
            Submits or updates the grade for a specific student in a specific subject.
        """
        db = get_db()
        try:
            db.grades.update_one(
                {"student_id": grade_submission.student_id, "subject": grade_submission.subject},
                {"$set": {"grade": grade_submission.grade}},
                upsert=True
            )
        except PyMongoError as e:
            return {"error": f"Failed to submit grade: {str(e)}"}

    @staticmethod
    def get_grades_by_subject(subject: str):
        """
            Retrieves statistics for a specific subject, including:
            - Number of students graded.
            - Average grade.
            - Median grade
        """
        db = get_db()
        try:
            grades = db.grades.find({"subject": subject})
            grade_list = [g['grade'] for g in grades]

            if not grade_list:
                return {"error": f"No grades found for the subject '{subject}'"}

            avg_grade = sum(grade_list) / len(grade_list)
            sorted_grades = sorted(grade_list)
            mid = len(sorted_grades) // 2

            if len(sorted_grades) % 2 == 0:
                median_grade = (sorted_grades[mid - 1] + sorted_grades[mid]) / 2
            else:
                median_grade = sorted_grades[mid]

            return {
                "subject": subject,
                "students_count": len(grade_list),
                "average_grade": avg_grade,
                "median_grade": median_grade
            }

        except PyMongoError as e:
            return {"error": f"Failed to retrieve grades for subject: {str(e)}"}

    @staticmethod
    def get_grades_by_student(student_id: str):
        """
            Retrieves all grades for a specific student and their average grade.
        """
        db = get_db()
        try:
            grades = db.grades.find({"student_id": student_id})
            grade_dict = {g['subject']: g['grade'] for g in grades}

            if not grade_dict:
                return {"error": f"No grades found for student '{student_id}'"}

            avg_grade = sum(grade_dict.values()) / len(grade_dict)
            return {
                "student_id": student_id,
                "grades": grade_dict,
                "average_grade": avg_grade
            }

        except PyMongoError as e:
            return {"error": f"Failed to retrieve grades for student: {str(e)}"}
