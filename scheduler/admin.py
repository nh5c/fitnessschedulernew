# scheduler/admin.py
from django.contrib import admin
from .models import WorkoutType, WorkoutSession


@admin.register(WorkoutType)
class WorkoutTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "default_duration_minutes", "intensity_level")


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ("title", "workout_type", "date", "start_time", "duration_minutes", "intensity")
    list_filter = ("workout_type", "date")
