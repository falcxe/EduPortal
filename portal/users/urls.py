from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test
from .views import login, registration, profile, reset_password, logout, apply_for_teacher, approve_teacher, reject_teacher

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('reset_password/', reset_password, name='reset_password'),
    path('logout/', logout, name='logout'),
    path('apply-for-teacher/', apply_for_teacher, name='apply_for_teacher'),
    path('approve-teacher/<int:user_id>/', login_required(user_passes_test(lambda u: u.is_staff)(approve_teacher)), name='approve_teacher'),
    path('reject-teacher/<int:user_id>/', login_required(user_passes_test(lambda u: u.is_staff)(reject_teacher)), name='reject_teacher'),
]