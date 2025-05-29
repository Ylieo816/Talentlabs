from django.core.management.base import BaseCommand
from jobs.models import Job
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = '生成20筆測試職位資料'

    def handle(self, *args, **kwargs):
        # 公司列表
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

        # 職位列表
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

        # 地點列表
        locations = [
            "Taipei, Taiwan",
            "New Taipei, Taiwan",
            "Taichung, Taiwan",
            "Kaohsiung, Taiwan",
            "Hsinchu, Taiwan"
        ]

        # 技能列表
        all_skills = [
            "Python", "JavaScript", "React", "Vue", "Angular",
            "Django", "Flask", "Node.js", "TypeScript", "Java",
            "Spring Boot", "PostgreSQL", "MongoDB", "Docker",
            "Kubernetes", "AWS", "Azure", "GCP", "CI/CD",
            "Git", "REST API", "GraphQL", "Microservices"
        ]

        # 薪資範圍
        salary_ranges = [
            "60,000 - 90,000 TWD",
            "80,000 - 120,000 TWD",
            "100,000 - 150,000 TWD",
            "120,000 - 180,000 TWD",
            "150,000 - 200,000 TWD"
        ]

        # 生成20筆資料
        for i in range(20):
            # 隨機選擇發布日期（過去30天到未來30天）
            posting_date = date.today() + timedelta(days=random.randint(-30, 30))
            # 隨機選擇過期日期（發布日期後30-90天）
            expiration_date = posting_date + timedelta(days=random.randint(30, 90))
            
            # 隨機選擇2-4個技能
            required_skills = random.sample(all_skills, random.randint(2, 4))
            
            # 創建職位
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