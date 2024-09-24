# Student Grading System

## Overview
The **Student Grading System** is a microservice-based web application that allows users to submit and retrieve student grades. It is built using Flask, MongoDB, Docker, and is designed for scalability and consistency. The system allows multiple instances to run simultaneously and synchronize data across all instances.

## Features
- **Submit Grades**: Submit student grades for different subjects.
- **Retrieve Grades by Subject**: Get the count, average, and median of student grades for a specific subject.
- **Retrieve Grades by Student**: Retrieve all grades for a specific student, along with their average.
- **Scaling**: Multiple instances can be spun up to support higher loads.
- **Containerization**: The application is fully containerized using Docker.

## Requirements
- Docker
- Docker Compose
- Python 3.9+
- MongoDB

## Project Structure
```bash
├── app/
│   ├── __init__.py           # Application factory
│   ├── routes.py             # API routes
│   ├── models.py             # Pydantic models
│   ├── services.py           # Service layer to handle logic
│   ├── db.py                 # MongoDB connection
├── tests/
│   ├── test_routes.py        # Unit and integration tests for API routes
├── Dockerfile                # Dockerfile to containerize the Flask app
├── docker-compose.yml        # Docker Compose configuration
├── haproxy.cfg               # HAProxy configuration for load balancing
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
```



# Student Grading System

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/student-grading-system.git
cd student-grading-system
```

### 2. Build Docker Containers

To build the Docker containers, run:

```bash
docker-compose build
```

## Running the Application

### 1. Start Services

To start the application along with MongoDB and load balancer (HAProxy), run:

```bash
docker-compose up
```

This will spin up the following services:
* **MongoDB**: Running on port 27017.
* **Grading Service**: Running two instances on ports 8000 and 8001.
* **HAProxy**: Load balancer running on port 80.

### 2. Access the API

### 1. Root Endpoint

* **GET /**: Returns a welcome message.

**Response**:
```json
{
  "message": "Welcome to the Student Grading System!"
}
```

### 2. Submit a Grade

* **POST /grades/submit**: Submits a grade for a student in a specific subject.

**Request**:
```json
{
  "student_id": "12345",
  "subject": "Math",
  "grade": 85
}
```

**Response**:
   * Success: `201 Created`
   * Validation Error: `400 Bad Request`

### 3. Get Grades by Subject

* **GET /grades/subject/<subject>**: Retrieves the count, average, and median of grades for a specific subject.

**Response**:
```json
{
  "subject": "Math",
  "student_count": 10,
  "average_grade": 85.5,
  "median_grade": 88
}
```

### 4. Get Grades by Student

* **GET /grades/student/<student_id>**: Retrieves all grades for a specific student, including the average grade.

**Response**:
```json
{
  "student_id": "12345",
  "grades": {
    "Math": 85,
    "Science": 90
  },
  "average_grade": 87.5
}
```

## Scaling

The system is designed to be scalable. Multiple instances of the grading service can be spun up by adding more instances in the `docker-compose.yml` file. HAProxy will balance the incoming requests across these instances to ensure that the system can handle high loads efficiently.

In the current setup, two instances of `grading_service` are defined: one running on port 8000 and another on port 8001. You can increase or decrease the number of instances as needed by adding/removing entries in the `docker-compose.yml`.


## Running Tests

To run tests in the `grading_service_test` container:

```bash
docker-compose run grading_service_test
```

The test suite includes unit and integration tests to ensure the functionality of the API endpoints.



