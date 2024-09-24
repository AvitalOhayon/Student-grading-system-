import uuid


def test_home_route(client):
    """
    Test the root route (GET /) to ensure it returns the correct welcome message.
    """
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Welcome to the Student Grading System!"


def test_submit_grade(client, db):
    """
    Test submitting a valid grade to the /grades/submit route and check if the data is correctly stored.
    """
    data = {
        "student_id": str(uuid.uuid4()),
        "subject": "Math",
        "grade": 95,
        "is_test_data": True
    }

    response = client.post('/grades/submit', json=data)
    assert response.status_code == 201

    result = db.grades.find_one({"student_id": data["student_id"]})
    assert result is not None
    assert result["grade"] == data["grade"]


def test_submit_invalid_grade(client):
    """
    Test submitting an invalid grade (outside of allowed range) to the /grades/submit route
    and verify the response contains appropriate validation errors.
    """
    data = {
        "student_id": str(uuid.uuid4()),
        "subject": "Math",
        "grade": 105,
        "is_test_data": True
    }

    response = client.post('/grades/submit', json=data)
    assert response.status_code == 400

    errors = response.get_json()
    assert "grade" in errors[0]["loc"]
    assert errors[0]["msg"] == "Input should be less than or equal to 100"


def test_get_grades_by_student(client, db):
    """
    Test retrieving grades by student ID from /grades/student/<student_id>
    and ensure the response contains the correct grades and average grade.
    """
    student_id = str(uuid.uuid4())
    db.grades.insert_one({
        "student_id": student_id,
        "subject": "Math",
        "grade": 90,
        "is_test_data": True
    })
    db.grades.insert_one({
        "student_id": student_id,
        "subject": "Science",
        "grade": 85,
        "is_test_data": True
    })

    response = client.get(f'/grades/student/{student_id}')
    assert response.status_code == 200

    result = response.get_json()
    assert len(result["grades"]) == 2
    assert result["grades"]["Math"] == 90
    assert result["grades"]["Science"] == 85
    assert result["average_grade"] == 87.5


def test_get_grades_by_subject(client, db):
    """
    Test retrieving grades by subject from /grades/subject/<subject> and check
    that the correct student count, average, and median grades are returned.
    """
    student_ids = [str(uuid.uuid4()) for _ in range(3)]
    for student_id in student_ids:
        db.grades.insert_one({
            "student_id": student_id,
            "subject": "YYY",
            "grade": 80,
            "is_test_data": True
        })

    response = client.get('/grades/subject/YYY')
    assert response.status_code == 200

    result = response.get_json()
    assert result["student_count"] == 3
    assert result["average_grade"] == 80
    assert result["median_grade"] == 80
