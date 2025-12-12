# scheduler/forms.py
from django import forms
from .models import WorkoutSession, WorkoutType


class WorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = [
            "title",
            "workout_type",
            "date",
            "start_time",
            "duration_minutes",
            "intensity",
            "notes",
        ]
    # Use HTML date/time inputs
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
        }


class ReportFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Start date",
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="End date",
    )
    workout_type = forms.ModelChoiceField(
        queryset=WorkoutType.objects.none(),
        required=False,
        empty_label="All workout types",
        label="Workout type",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This is where the dropdown is built dynamically from the DB
        self.fields["workout_type"].queryset = WorkoutType.objects.all()
