# Generated by Django 5.1 on 2024-10-25 12:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0004_remove_license_user_license_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='license.group'),
        ),
    ]
