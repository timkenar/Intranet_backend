# Generated by Django 5.1 on 2024-10-25 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='allowed_apps',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='features',
            field=models.JSONField(default=list),
        ),
    ]
