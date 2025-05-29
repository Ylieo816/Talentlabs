from django.core.management.base import BaseCommand
from jobs.models import Job
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Generate 120 test job data'

    def handle(self, *args, **kwargs):
        # Company Choices
        companies = [
            "Tech Solutions Inc.",
            "Digital Innovations",
            "Future Systems",
            "Smart Tech",
            "Global Software",
            "Innovative Solutions",
            "Tech Pioneers",
            "Digital Dynamics",
            "Future Technologies",
            "Smart Systems"
        ]

        # Position Choices
        job_titles = [
            "Senior Python Developer",
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer",
            "DevOps Engineer",
            "Data Scientist",
            "Machine Learning Engineer",
            "Mobile Developer",
            "UI/UX Designer",
            "Product Manager"
        ]

        # Location Choices
        locations = [
            "Taipei, Taiwan",
            "New Taipei, Taiwan",
            "Taichung, Taiwan",
            "Kaohsiung, Taiwan",
            "Hsinchu, Taiwan"
        ]

        # Skill Choices
        all_skills = [
            "Python", "JavaScript", "React", "Vue", "Angular",
            "Django", "Flask", "Node.js", "TypeScript", "Java",
            "Spring Boot", "PostgreSQL", "MongoDB", "Docker",
            "Kubernetes", "AWS", "Azure", "GCP", "CI/CD",
            "Git", "REST API", "GraphQL", "Microservices"
        ]

        # Salary Range Choices
        salary_ranges = [
            "60,000 - 90,000 TWD",
            "80,000 - 120,000 TWD",
            "100,000 - 150,000 TWD",
            "120,000 - 180,000 TWD",
            "150,000 - 200,000 TWD"
        ]

        # Generate 120 test data
        for i in range(120):
            # Randomly select posting date (60 days ago to 60 days from now)
            posting_date = date.today() + timedelta(days=random.randint(-60, 60))
            # Randomly select expiration date (30-90 days after posting date)
            expiration_date = posting_date + timedelta(days=random.randint(30, 90))
            
            # Randomly select 2-4 skills
            required_skills = random.sample(all_skills, random.randint(2, 4))
            
            # Create job
            job = Job.objects.create(
                title=random.choice(job_titles),
                company=random.choice(companies),
                location=random.choice(locations),
                description=f"This is a test job posting #{i+1}. We are looking for a talented professional to join our team.",
                salary_range=random.choice(salary_ranges),
                required_skills=required_skills,
                posting_date=posting_date,
                expiration_date=expiration_date
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created job: {job.title} at {job.company}')
            ) 