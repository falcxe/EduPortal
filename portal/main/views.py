from django.shortcuts import render
from courses.models import Course

def index(request):
    new_courses = Course.objects.order_by('-created_at')[:4]
    recommended_courses = Course.objects.filter(author__username='falcxe')[:4]

    context = {
        'new_courses': new_courses,
        'recommended_courses': recommended_courses
    }
    return render(request, 'main/index.html', context)