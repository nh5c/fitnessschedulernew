# scheduler/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Avg, Count
from .models import WorkoutSession
from .forms import WorkoutSessionForm, ReportFilterForm


def session_list(request):
    """List all workout sessions (main page)."""
    sessions = WorkoutSession.objects.select_related("workout_type").all()
    return render(request, "scheduler/session_list.html", {"sessions": sessions})


def session_create(request):
    """Create a new workout session (Requirement 1 - insert)."""
    if request.method == "POST":
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            return redirect("session_list")
    else:
        form = WorkoutSessionForm()
    return render(
        request,
        "scheduler/session_form.html",
        {"form": form, "is_edit": False},
    )


def session_update(request, pk):
    """Edit an existing workout session (Requirement 1 - update)."""
    session = get_object_or_404(WorkoutSession, pk=pk)
    if request.method == "POST":
        form = WorkoutSessionForm(request.POST, instance=session)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            return redirect("session_list")
    else:
        form = WorkoutSessionForm(instance=session)
    return render(
        request,
        "scheduler/session_form.html",
        {"form": form, "is_edit": True},
    )


def session_delete(request, pk):
    """Delete a workout session (Requirement 1 - delete)."""
    session = get_object_or_404(WorkoutSession, pk=pk)
    if request.method == "POST":
        with transaction.atomic():
            session.delete()
        return redirect("session_list")
    return render(
        request,
        "scheduler/session_confirm_delete.html",
        {"session": session},
    )


def session_report(request):
    """
    Requirement 2:
    Filter data (by date range and workout type) and show a report with stats.
    """
    form = ReportFilterForm(request.GET or None)
    sessions = None
    stats = None

    if form.is_valid():
        sessions = WorkoutSession.objects.select_related("workout_type").all()

        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        workout_type = form.cleaned_data.get("workout_type")

        if start_date:
            sessions = sessions.filter(date__gte=start_date)
        if end_date:
            sessions = sessions.filter(date__lte=end_date)
        if workout_type:
            sessions = sessions.filter(workout_type=workout_type)

        stats = sessions.aggregate(
            total_sessions=Count("id"),
            avg_duration=Avg("duration_minutes"),
            avg_intensity=Avg("intensity"),
        )

    return render(
        request,
        "scheduler/report.html",
        {
            "form": form,
            "sessions": sessions,
            "stats": stats,
        },
    )
