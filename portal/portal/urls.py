from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import auth_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # Регистрация приложения main
    path('user/', include('users.urls')),
    path('catalog/', include('courses.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('auth-error/', auth_error, name='auth-error'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)