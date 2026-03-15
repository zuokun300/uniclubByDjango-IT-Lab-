from django.conf import settings
from django.db import models
from django.urls import reverse


class Club(models.Model):
    club_name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    founded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="founded_clubs",
    )

    class Meta:
        ordering = ["club_name"]

    def __str__(self):
        return self.club_name

    def get_absolute_url(self):
        return reverse("club_detail", args=[self.pk])


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="events")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_events",
    )

    class Meta:
        ordering = ["event_date", "event_name"]

    def __str__(self):
        return self.event_name


class Membership(models.Model):
    join_date = models.DateTimeField(auto_now_add=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["club", "user"], name="unique_club_membership"),
        ]


class Registration(models.Model):
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="registrations",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["event", "user"], name="unique_event_registration"),
        ]


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    class Meta:
        ordering = ["-created_at"]

