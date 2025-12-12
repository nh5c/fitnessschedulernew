# scheduler/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class WorkoutType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    default_duration_minutes = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(1)],
    )
    # 1 = very light, 5 = very intense
    intensity_level = models.PositiveIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    def __str__(self):
        return self.name


class WorkoutSession(models.Model):
    title = models.CharField(max_length=200)
    workout_type = models.ForeignKey(WorkoutType, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    # 1-5 scale. You can say this is "how hard it felt".
    intensity = models.PositiveIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date", "-start_time"]
        indexes = [
            models.Index(fields=["date"], name="session_date_idx"),
            models.Index(fields=["workout_type", "date"], name="session_type_date_idx"),
        ]

    def __str__(self):
        return f"{self.title} on {self.date}"
