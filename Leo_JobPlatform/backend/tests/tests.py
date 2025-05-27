from django.test import TestCase
from django.test import Client
from datetime import date, timedelta
from jobs.models import Job
import json

class JobAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # create multiple test jobs
        self.job1 = Job.objects.create(
            title="Senior Python Developer",
            company="Tech Corp",
            location="Taipei, Taiwan",
            description="We are looking for a senior Python developer...",
            salary_range="80,000 - 120,000 TWD",
            required_skills=["Python", "Django", "PostgreSQL"],
            posting_date=date.today() + timedelta(days=1),  # post in the future
            expiration_date=date.today() + timedelta(days=31),
        )
        self.job2 = Job.objects.create(
            title="Frontend Developer",
            company="Web Solutions",
            location="Kaohsiung, Taiwan",
            description="Looking for a frontend developer...",
            salary_range="60,000 - 90,000 TWD",
            required_skills=["React", "TypeScript", "CSS"],
            posting_date=date.today(),  # post today
            expiration_date=date.today() + timedelta(days=29),
        )
        self.job3 = Job.objects.create(
            title="DevOps Engineer",
            company="Cloud Tech",
            location="Taipei, Taiwan",
            description="DevOps engineer needed...",
            salary_range="90,000 - 130,000 TWD",
            required_skills=["Docker", "Kubernetes", "AWS"],
            posting_date=date.today() - timedelta(days=2),  # post in the past
            expiration_date=date.today() - timedelta(days=1),
        )

    def test_list_jobs(self):
        response = self.client.get('/api/jobs')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

    def test_list_jobs_with_filters(self):
        # filter by search keyword
        response = self.client.get('/api/jobs?search=Python')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], "Senior Python Developer")

        # filter by status
        response = self.client.get('/api/jobs?status=scheduled')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], "Senior Python Developer")

        # filter by location
        response = self.client.get('/api/jobs?location=Taipei')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

        # filter by company
        response = self.client.get('/api/jobs?company=Tech')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['company'], "Tech Corp")

    def test_list_jobs_pagination(self):
        # pagination
        response = self.client.get('/api/jobs?page=1&page_size=2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

        # test second page
        response = self.client.get('/api/jobs?page=2&page_size=2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    def test_list_jobs_ordering(self):
        # order by posting date
        response = self.client.get('/api/jobs?order_by=posting_date')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)
        # check if the jobs are ordered by posting date in descending order
        self.assertEqual(data[0]['title'], "Senior Python Developer")
        self.assertEqual(data[1]['title'], "Frontend Developer")
        self.assertEqual(data[2]['title'], "DevOps Engineer")

    def test_get_job(self):
        response = self.client.get(f'/api/jobs/{self.job1.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], "Senior Python Developer")

    def test_create_job(self):
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
        response = self.client.delete(f'/api/jobs/{self.job1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Job.objects.count(), 2)
