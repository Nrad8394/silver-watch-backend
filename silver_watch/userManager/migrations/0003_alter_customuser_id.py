# Generated by Django 5.1.6 on 2025-02-21 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userManager', '0002_alter_customuser_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.CharField(editable=False, max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
