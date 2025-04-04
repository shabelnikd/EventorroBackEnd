# Generated by Django 4.1.5 on 2023-04-21 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_remove_event_main_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='age_limits',
            field=models.CharField(choices=[('1', 'Без ограничений'), ('2', '16+'), ('3', '18+'), ('4', '21+')], max_length=50),
        ),
        migrations.AlterField(
            model_name='event',
            name='audience',
            field=models.CharField(choices=[('1', 'Для всех'), ('2', 'Для детей'), ('3', 'Для женщин'), ('4', 'Для мужчин')], max_length=50),
        ),
    ]
