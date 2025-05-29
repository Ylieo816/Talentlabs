from datetime import datetime
from ninja import Schema
from typing import List
from typing import Optional

class JobSchema(Schema):
    id: int
    title: str
    company: str
    location: str
    description: str
    salary_range: str = None
    required_skills: List[str]
    posting_date: datetime
    expiration_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime

class JobCreateSchema(Schema):
    title: str
    company: str
    location: str
    description: str
    salary_range: str = None
    required_skills: List[str]
    posting_date: datetime
    expiration_date: datetime

class JobQueryParams(Schema):
    search: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None
    order_by: Optional[str] = "posting_date"
    page: int = 1
    page_size: int = 10

class PaginatedResponse(Schema):
    items: List[JobSchema]
    total: int
    page: int
    page_size: int
    total_pages: int