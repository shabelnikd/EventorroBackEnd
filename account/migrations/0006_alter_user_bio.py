# Generated by Django 4.1.5 on 2023-05-04 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_user_telegram_remove_user_whatsapp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, max_length=700, null=True),
        ),
    ]
