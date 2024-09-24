from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models import GradeSubmission, SubjectGrades, StudentGrades
from app.services import GradeService


app_routes = Blueprint('app_routes', __name__)


@app_routes.route('/')
def home():
    """
    Home route to welcome the users to the Student Grading System.
    """
    return jsonify({"message": "Welcome to the Student Grading System!"})


@app_routes.route('/grades/submit', methods=['POST'])
def submit_grade():
    """
    Submits a grade for a student in a specific subject using the GradeSubmission model.

    Request body (JSON):
    - student_id: str, the unique ID of the student.
    - subject: str, the subject name.
    - grade: int, the grade value between 0 and 100.

    Response:
    - Success: 201 Created, with a success message.
    - Failure: 400 Bad Request, with an error message if validation fails.
    """
    try:
        # Validate the input data using the GradeSubmission model
        grade_submission = GradeSubmission(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    # Pass the validated model to the service
    GradeService.submit_grade(grade_submission)

    return jsonify({"message": "Grade submitted successfully"}), 201


@app_routes.route('/grades/subject/<string:subject>', methods=['GET'])
def get_grades_by_subject(subject):
    """
    Retrieves grades for a specific subject, including:
    - Number of students graded in that subject.
    - Average grade.
    - Median grade.

    Response:
    - Success: 200 OK, with subject statistics.
    """
    subject_stats = GradeService.get_grades_by_subject(subject)

    # Build the response using the SubjectGrades model
    response = SubjectGrades(
        subject=subject,
        student_count=subject_stats['students_count'],
        average_grade=subject_stats['average_grade'],
        median_grade=subject_stats['median_grade']
    )

    return jsonify(response.dict()), 200


@app_routes.route('/grades/student/<string:student_id>', methods=['GET'])
def get_grades_by_student(student_id):
    """
    Retrieves grades for a specific student across all subjects.
    The response includes the student's average grade.

    Response:
    - Success: 200 OK, with student grades and their average.
    """
    student_data = GradeService.get_grades_by_student(student_id)

    # Build the response using the StudentGrades model
    response = StudentGrades(
        student_id=student_id,
        grades=student_data['grades'],
        average_grade=student_data['average_grade']
    )

    return jsonify(response.dict()), 200
