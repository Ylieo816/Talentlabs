# Job Platform

This project is developed for TalentLabs Coding Assignment: Job Platform.

Developer: Leo Yao

## Features and Tech Stack

### Backend (focus)
- Django (Python) with Django Ninja framework
- PostgreSQL database
- Docker for containerization
- (Future Plan) Celery for asynchronous task processing
- (Future Plan) Redis for message broker and caching

### Frontend (React)
- **Job Listing Page** (`http://localhost:3000/`)
  - View all available job postings
  - Search jobs by keywords
  - Filter jobs by:
    - Status (active, scheduled, expired)
    - Location
    - Company
  - Sort jobs by posting date
  - Pagination support
  - Click on job cards to view details
  - Responsive design for all screen sizes

- **Job Detail Page** (`http://localhost:3000/jobs/:id`)
  - View complete job information
  - Display job title, company, location
  - Show salary range
  - List required skills
  - View posting and expiration dates
  - Back button to return to job list

- **Job Creation Page** (`http://localhost:3000/create`)
  - Form to create new job postings
  - Input validation
  - Required fields checking

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker
- Docker Compose

## Getting Started

### 1. Clone the repository
```bash
git clone git@github.com:Ylieo816/Talentlabs.git
cd Leo_JobPlatform
```

### 2. Start the application
```bash
docker compose up
```
This will start the backend server and PostgreSQL database.

### 3. Running Local Tests for Backend only
To run the test suite, use the following command:
```bash
docker compose run --rm backend pytest tests/tests.py -v
```

The test suite includes:
- Job creation
- Job listing: search all with filters, sorting, pagination
- Job updating
- Job deletion

## API Documentation

Once the application is running locally, you can access the interactive API documentation at:
```
http://localhost:8000/api/docs
```

This documentation provides:
- Detailed API endpoint descriptions
- Request/response schemas
- Interactive testing interface
- Example requests and responses

## Asynchronous Processing Future Plan

The project will use Celery and Celery Beat for handling asynchronous tasks in the future:

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
Leo_JobPlatform/
├── backend/               # Django + API + PostgreSQL
│   ├── jobs/
│   │   ├── apis.py        # API endpoints
│   │   ├── models.py      # Database models
│   │   └── schemas.py     # Pydantic schemas
│   ├── tests/
│   │   └── tests.py       # Test cases
│   └── job_platform/      # Django project settings
├── frontend/              # React + Vite
│   ├── src/components/
│   │   ├── JobDetail.tsx  # Show specific job
│   │   ├── JobForm.tsx    # User input for new job post
│   │   └── JobList.tsx    # List all jobs
└── docker-compose.yml     # Manage Docker package for fullstack
```

## Development Status

Currently, the project has completed the implementation with the following features:
Backend:
- RESTful API endpoints for job management
- Database models and schemas
- Comprehensive test coverage for backend APIs
- Docker configuration for easy deployment

Frontend:
- Built with React and TypeScript
- Modern UI with responsive design
- State management with React Hooks
- Routing with React Router
- HTTP requests with Axios