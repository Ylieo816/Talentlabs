# Job Platform

This project is developed for TalentLabs Coding Assignment: Job Platform.

Developer: Leo Yao

## Tech Stack

### Backend
- Django (Python) with Django Ninja framework
- PostgreSQL database
- Docker for containerization
- Celery for asynchronous task processing
- Redis for message broker and caching

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker
- Docker Compose

## Getting Started

### 1. Clone the repository
```bash
git clone <repository-url>
cd Leo_JobPlatform
```

### 2. Start the application
```bash
docker compose up
```
This will start the backend server and PostgreSQL database.

### 3. Running Tests
To run the test suite, use the following command:
```bash
docker compose run --rm web pytest tests/tests.py -v
```

The test suite includes:
- Job creation
- Job listing with filters
- Job updating
- Job deletion
- Pagination
- Sorting
- Search functionality

## API Documentation

Once the application is running, you can access the interactive API documentation at:
```
http://localhost:8000/api/docs
```

This documentation provides:
- Detailed API endpoint descriptions
- Request/response schemas
- Interactive testing interface
- Example requests and responses

## Asynchronous Processing

The project uses Celery and Celery Beat for handling asynchronous tasks:

### Scheduled Tasks
- Job status updates based on posting and expiration dates
- Automatic status transitions (scheduled → active → expired)
- Regular data cleanup and maintenance

### Background Jobs
- Email notifications for job status changes
- Data aggregation and reporting
- Cache invalidation and updates

## Cloud Deployment (AWS)

The application is designed further to be deployed on AWS with the following services:

### Infrastructure
- **ECS (Elastic Container Service)**: For running Docker containers and Celery
- **RDS**: For PostgreSQL database
- **ElastiCache**: For Redis message broker and caching
- **S3**: For static file storage
- **SQS**: For async message queue

### Monitoring and Logging
- **CloudWatch**: For monitoring and logging
- **X-Ray**: For request tracing
- **CloudTrail**: For API activity logging

### Security
- **IAM**: For access management
- **VPC**: For network isolation
- **ACM**: For SSL/TLS certificates

## Project Structure

```
backend/
├── jobs/
│   ├── apis.py      # API endpoints
│   ├── models.py    # Database models
│   └── schemas.py   # Pydantic schemas
├── tests/
│   └── tests.py     # Test cases
└── job_platform/    # Django project settings
```

## Development Status

Currently, the project has completed the backend implementation with the following features:
- RESTful API endpoints for job management
- Database models and schemas
- Comprehensive test coverage
- Docker configuration for easy deployment
- Asynchronous task processing setup
- Cloud deployment configuration

Frontend development is planned for future implementation.
