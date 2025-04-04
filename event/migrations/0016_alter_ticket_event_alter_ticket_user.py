# Generated by Django 4.1.5 on 2023-05-07 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0015_alter_ticket_event_alter_ticket_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='event.event'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
