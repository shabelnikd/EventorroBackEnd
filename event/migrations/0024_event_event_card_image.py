# Generated by Django 4.1.5 on 2023-07-15 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0023_event_location_name_alter_event_location_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_card_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
