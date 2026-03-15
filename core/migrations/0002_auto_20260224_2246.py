from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="membership",
            constraint=models.UniqueConstraint(fields=("club", "user"), name="unique_club_membership"),
        ),
        migrations.AddConstraint(
            model_name="registration",
            constraint=models.UniqueConstraint(fields=("event", "user"), name="unique_event_registration"),
        ),
    ]

