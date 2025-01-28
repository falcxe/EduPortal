from django.contrib import admin
from .models import Course, Comment

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'subject')
    list_filter = ('grade', 'subject')
    search_fields = ('name', 'description')

admin.site.register(Course, CourseAdmin)
admin.site.register(Comment)  # Регистрация модели Comment