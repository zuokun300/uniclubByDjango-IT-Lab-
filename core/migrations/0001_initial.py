from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Club",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("club_name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "founded_by",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="founded_clubs", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["club_name"]},
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("event_name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("event_date", models.DateTimeField()),
                ("location", models.CharField(max_length=150)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "club",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="events", to="core.club"),
                ),
                (
                    "created_by",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="created_events", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["event_date", "event_name"]},
        ),
        migrations.CreateModel(
            name="Membership",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("join_date", models.DateTimeField(auto_now_add=True)),
                (
                    "club",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="core.club"),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Registration",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")], default="pending", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "event",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="registrations", to="core.event"),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="registrations", to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
    ]

