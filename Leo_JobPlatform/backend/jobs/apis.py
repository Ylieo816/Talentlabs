from typing import List
from ninja import Router, Query
from django.shortcuts import get_object_or_404
from django.db import models
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .models import Job
from .schemas import JobSchema, JobCreateSchema, JobQueryParams, PaginatedResponse
import math

router = Router()

# Create a new job posting
@router.post("/jobs", response=JobSchema)
def create_job(request, payload: JobCreateSchema):
    try:
        job = Job.objects.create(**payload.dict())
        return job
    except IntegrityError as e:
        raise ValidationError("Invalid job data: " + str(e))
    except Exception as e:
        raise ValidationError("Failed to create job: " + str(e))

# List jobs with filtering, sorting and pagination
@router.get("/jobs", response=PaginatedResponse)
def list_jobs(request, params: JobQueryParams = Query(...)):
    try:
        qs = Job.objects.all()

        # Apply search filters
        if params.search:
            qs = qs.filter(
                models.Q(title__icontains=params.search) |
                models.Q(description__icontains=params.search) |
                models.Q(company__icontains=params.search)
            )

        # Apply status filter
        if params.status:
            qs = qs.filter(status__iexact=params.status)

        # Apply location and company filters
        if params.location:
            qs = qs.filter(location__icontains=params.location)
        if params.company:
            qs = qs.filter(company__icontains=params.company)

        # Apply sorting
        if params.order_by == "posting_date":
            qs = qs.order_by("-posting_date")  # newest first
        elif params.order_by == "expiration_date":
            qs = qs.order_by("expiration_date")  # earliest expiration first

        # Calculate pagination
        total = qs.count()
        if params.page_size <= 0:
            params.page_size = total  # return all items if page_size is invalid
        
        total_pages = math.ceil(total / params.page_size) if params.page_size > 0 else 1
        
        # Validate page number
        if params.page < 1:
            params.page = 1
        elif params.page > total_pages and total_pages > 0:
            params.page = total_pages
        
        # Get paginated results
        start = (params.page - 1) * params.page_size
        end = start + params.page_size
        items = list(qs[start:end])
        
        return {
            "items": items,
            "total": total,
            "page": params.page,
            "page_size": params.page_size,
            "total_pages": total_pages
        }
    except Exception as e:
        raise ValidationError("Failed to fetch jobs: " + str(e))

# Get a single job by ID
@router.get("/jobs/{job_id}", response=JobSchema)
def get_job(request, job_id: int):
    try:
        return get_object_or_404(Job, id=job_id)
    except Exception as e:
        raise ValidationError("Failed to fetch job: " + str(e))

# Update an existing job
@router.put("/jobs/{job_id}", response=JobSchema)
def update_job(request, job_id: int, payload: JobCreateSchema):
    try:
        job = get_object_or_404(Job, id=job_id)
        update_data = payload.dict()
        update_data.pop("company", None)  # prevent company name updates
        for key, value in update_data.items():
            setattr(job, key, value)
        job.save()
        return job
    except IntegrityError as e:
        raise ValidationError("Invalid job data: " + str(e))
    except Exception as e:
        raise ValidationError("Failed to update job: " + str(e))

# Delete a job
@router.delete("/jobs/{job_id}")
def delete_job(request, job_id: int):
    try:
        job = get_object_or_404(Job, id=job_id)
        job.delete()
        return {"success": True}
    except Exception as e:
        raise ValidationError("Failed to delete job: " + str(e)) 