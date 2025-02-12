from django.contrib import admin
from .models import Course, CourseMaterial, Comment

class CourseMaterialInline(admin.TabularInline):
    model = CourseMaterial
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'subject')
    list_filter = ('grade', 'subject')
    search_fields = ('name', 'description')
    inlines = [CourseMaterialInline]

admin.site.register(Course, CourseAdmin)
admin.site.register(Comment)