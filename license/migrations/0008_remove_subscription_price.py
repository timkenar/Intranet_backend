# Generated by Django 5.1 on 2024-10-25 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0007_remove_group_tenant_remove_group_users_delete_tenant_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='price',
        ),
    ]
