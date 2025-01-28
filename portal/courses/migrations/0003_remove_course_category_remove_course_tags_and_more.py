# Generated by Django 5.1.4 on 2024-12-31 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_tag_course_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='category',
        ),
        migrations.RemoveField(
            model_name='course',
            name='tags',
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, default='main/img/default_course_image.jpg', null=True, upload_to='courses_images/'),
        ),
        migrations.DeleteModel(
            name='CourseCategory',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
