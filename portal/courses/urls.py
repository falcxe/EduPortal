from . import views
from django.urls import path
from .views import CourseDetailView, CourseUpdateView, CourseDeleteView, DeleteCommentView

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('create', views.create, name='create'),
    path('<int:pk>', CourseDetailView.as_view(), name='course-detail'),
    path('<int:pk>/edit', CourseUpdateView.as_view(), name='course-edit'),
    path('<int:pk>/delete', CourseDeleteView.as_view(), name='course-delete'),
    path('course/<int:pk>/download-all/', views.download_all_materials, name='download-all-materials'),
    path('comment/<int:pk>/delete/', DeleteCommentView.as_view(), name='delete-comment'),
    path('comment/<int:pk>/reply/', views.add_reply, name='add-reply'),
]