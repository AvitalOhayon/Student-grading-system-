from pydantic import BaseModel, Field


class GradeSubmission(BaseModel):
    """
    Model representing the submission of a grade.

    Attributes:
    - student_id (str): The unique identifier of the student.
    - subject (str): The name of the subject.
    - grade (int): The grade value, constrained between 0 and 100.
    """
    student_id: str
    subject: str
    grade: int = Field(..., ge=0, le=100)  # Grade must be between 0 and 100.


class SubjectGrades(BaseModel):
    """
    Model representing the statistics for grades in a specific subject.

    Attributes:
    - subject (str): The name of the subject.
    - student_count (int): The number of students graded in this subject.
    - average_grade (float): The average grade in the subject.
    - median_grade (float): The median grade in the subject.
    """
    subject: str
    student_count: int
    average_grade: float
    median_grade: float


class StudentGrades(BaseModel):
    """
    Model representing the grades of a student across all subjects.

    Attributes:
    - student_id (str): The unique identifier of the student.
    - grades (dict): A dictionary mapping subjects to grades.
    - average_grade (float): The student's average grade across all subjects.
    """
    student_id: str
    grades: dict[str, int]
    average_grade: float
