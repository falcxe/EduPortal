# Generated by Django 5.1.4 on 2025-01-20 19:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_course_materials_alter_course_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='materials',
        ),
        migrations.CreateModel(
            name='CourseMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='course_materials/', verbose_name='Файл')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='courses.course')),
            ],
        ),
    ]
