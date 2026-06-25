import uuid

from django.db import migrations, models


def populate_public_tokens(apps, schema_editor):
    Appointment = apps.get_model("bookings", "Appointment")

    for appointment in Appointment.objects.filter(public_token__isnull=True):
        appointment.public_token = uuid.uuid4()
        appointment.save(update_fields=["public_token"])


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0007_alter_appointment_service"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="public_token",
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.RunPython(populate_public_tokens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="appointment",
            name="public_token",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]