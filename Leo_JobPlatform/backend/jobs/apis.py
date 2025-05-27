from typing import List
from ninja import Router, Query
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Job
from .schemas import JobSchema, JobCreateSchema, JobQueryParams

router = Router()

@router.post("/jobs", response=JobSchema)
def create_job(request, payload: JobCreateSchema):
    job = Job.objects.create(**payload.dict())
    return job

@router.get("/jobs", response=List[JobSchema])
def list_jobs(request, params: JobQueryParams = Query(...)):
    qs = Job.objects.all()

    # Search by keyword
    if params.search:
        qs = qs.filter(
            models.Q(title__icontains=params.search) |
            models.Q(description__icontains=params.search) |
            models.Q(company__icontains=params.search)
        )

    # Filter by status
    if params.status:
        qs = qs.filter(status__iexact=params.status)

    # Filter by other fields
    if params.location:
        qs = qs.filter(location__icontains=params.location)
    if params.company:
        qs = qs.filter(company__icontains=params.company)

    # Order by
    if params.order_by in ["posting_date", "expiration_date"]:
        qs = qs.order_by(f"-{params.order_by}")  # order by descending

    # Pagination
    start = (params.page - 1) * params.page_size
    end = start + params.page_size
    return qs[start:end]

@router.get("/jobs/{job_id}", response=JobSchema)
def get_job(request, job_id: int):
    return get_object_or_404(Job, id=job_id)

@router.put("/jobs/{job_id}", response=JobSchema)
def update_job(request, job_id: int, payload: JobCreateSchema):
    job = get_object_or_404(Job, id=job_id)
    update_data = payload.dict()
    update_data.pop("company", None)  # restrict update company name
    for key, value in update_data.items():
        setattr(job, key, value)
    job.save()
    return job

@router.delete("/jobs/{job_id}")
def delete_job(request, job_id: int):
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return {"success": True} 