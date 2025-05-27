from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from jobs.apis import router as jobs_router

api = NinjaAPI()
api.add_router("/", jobs_router, tags=["jobs"])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]