from django.test import TestCase
from django.test import Client
from datetime import date, timedelta
from jobs.models import Job
import json
import warnings
import pytest

# Suppress all warnings during tests
@pytest.fixture(autouse=True)
def ignore_warnings():
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    warnings.filterwarnings('ignore', category=UserWarning)
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    warnings.filterwarnings('ignore', category=FutureWarning)

class JobAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test job postings with different statuses and dates
        self.job1 = Job.objects.create(
            title="Senior Python Developer",
            company="Tech Corp",
            location="Taipei, Taiwan",
            description="We are looking for a senior Python developer...",
            salary_range="80,000 - 120,000 TWD",
            required_skills=["Python", "Django", "PostgreSQL"],
            posting_date=date.today() + timedelta(days=1),  # post in the future
            expiration_date=date.today() + timedelta(days=31)
        )
        self.job2 = Job.objects.create(
            title="Frontend Developer",
            company="Web Solutions",
            location="Kaohsiung, Taiwan",
            description="Looking for a frontend developer...",
            salary_range="60,000 - 90,000 TWD",
            required_skills=["React", "TypeScript", "CSS"],
            posting_date=date.today(),  # post today
            expiration_date=date.today() + timedelta(days=29)
        )
        self.job3 = Job.objects.create(
            title="DevOps Engineer",
            company="Cloud Tech",
            location="Taipei, Taiwan",
            description="DevOps engineer needed...",
            salary_range="90,000 - 130,000 TWD",
            required_skills=["Docker", "Kubernetes", "AWS"],
            posting_date=date.today() - timedelta(days=2),  # post in the past
            expiration_date=date.today() - timedelta(days=1) # expired
        )

    def test_list_jobs(self):
        # Test basic job listing functionality
        response = self.client.get('/api/jobs')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['items']), 3)
        self.assertEqual(data['total'], 3)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['page_size'], 10)
        self.assertEqual(data['total_pages'], 1)

    def test_list_jobs_with_filters(self):
        # Test search functionality
        response = self.client.get('/api/jobs?search=Python')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['title'], "Senior Python Developer")

        # Test status filtering
        response = self.client.get('/api/jobs?status=scheduled')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['status'], "scheduled")

        # Test location filtering
        response = self.client.get('/api/jobs?location=Taipei')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['items']), 2)

        # Test company filtering
        response = self.client.get('/api/jobs?company=Tech%20Corp')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['company'], "Tech Corp")

    def test_list_jobs_with_ordering(self):
        # Test sorting by posting date
        response = self.client.get('/api/jobs?order_by=posting_date')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['items'][0]['title'], "Senior Python Developer")  # the job posted recently should be the first one

        # Test sorting by expiration date
        response = self.client.get('/api/jobs?order_by=expiration_date')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['items'][0]['title'], "DevOps Engineer")  # expired job should be the first one

    def test_list_jobs_with_pagination(self):
        # Create additional test data
        for i in range(15):  # create 15 more jobs
            Job.objects.create(
                title=f"Test Job {i}",
                company=f"Test Company {i}",
                location="Taipei, Taiwan",
                description=f"Test description {i}",
                salary_range="50,000 - 70,000 TWD",
                required_skills=["Test"],
                posting_date=date.today(),
                expiration_date=date.today() + timedelta(days=30),
                status="active"
            )

        # Test first page
        response = self.client.get('/api/jobs?page=1&page_size=10')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['items']), 10)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['total_pages'], 2)

        # Test second page
        response = self.client.get('/api/jobs?page=2&page_size=10')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['items']), 8)  # 18 jobs, the second page should have 8 jobs
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['total_pages'], 2)

    def test_list_jobs_with_invalid_page(self):
        # Test handling of invalid page number
        response = self.client.get('/api/jobs?page=999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['page'], 1)  # should be adjusted to the first page
        self.assertEqual(len(data['items']), 3)  # the first page should have 3 jobs
        self.assertEqual(data['total_pages'], 1)

    def test_list_jobs_with_invalid_page_size(self):
        # Test handling of invalid page size
        response = self.client.get('/api/jobs?page_size=0')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['items']), 3)  # should return all jobs
        self.assertEqual(data['page_size'], 3)  # should be adjusted to the total number
        self.assertEqual(data['total_pages'], 1)

    def test_list_jobs_with_invalid_order_by(self):
        # Test handling of invalid sorting parameter
        response = self.client.get('/api/jobs?order_by=invalid_field')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['items']), 3)  # should return all jobs, using default sorting

    def test_get_job(self):
        # Test retrieving a single job
        response = self.client.get(f'/api/jobs/{self.job1.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], "Senior Python Developer")

    def test_create_job(self):
        # Test creating a new job
        job_data = {
            "title": "Software Engineer",
            "company": "Dell",
            "location": "Taipei, Taiwan",
            "description": "New job description...",
            "salary_range": "70,000 - 100,000 TWD",
            "required_skills": ["Python", "Django"],
            "posting_date": date.today().isoformat(),
            "expiration_date": (date.today() + timedelta(days=30)).isoformat()
        }
        response = self.client.post(
            '/api/jobs',
            json.dumps(job_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], "Software Engineer")

    def test_update_job(self):
        # Test updating an existing job
        update_data = {
            "title": "Staff Python Developer",
            "company": self.job1.company,
            "location": "Taipei, Taiwan (Remote)",
            "description": "Updated job description...",
            "salary_range": "90,000 - 130,000 TWD",
            "required_skills": ["Python", "Django", "PostgreSQL", "AWS"],
            "posting_date": date.today().isoformat(),
            "expiration_date": (date.today() + timedelta(days=30)).isoformat()
        }
        response = self.client.put(
            f'/api/jobs/{self.job1.id}',
            json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], "Staff Python Developer")

    def test_delete_job(self):
        # Test deleting a job
        response = self.client.delete(f'/api/jobs/{self.job1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Job.objects.count(), 2)
