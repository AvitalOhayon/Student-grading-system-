import pytest
from pymongo import MongoClient


@pytest.fixture
def client():
    """
    Creates a test client for sending HTTP requests to the Flask app.
    """
    from app import create_app
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app.test_client()

@pytest.fixture
def db():
    """
    Connects to the regular MongoDB database.
    """
    client = MongoClient("mongodb://localhost:27017")
    db = client.mydatabase
    return db

@pytest.fixture(autouse=True)
def cleanup_after_test(db):
    """
    Automatically removes all test data from the database after each test.
    This fixture deletes all records with a UUID used during tests.
    """
    yield

    db.grades.delete_many({"is_test_data": True})
