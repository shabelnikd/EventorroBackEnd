# Generated by Django 4.1.5 on 2023-02-13 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_event_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventdate',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_dates', to='event.event'),
        ),
    ]
