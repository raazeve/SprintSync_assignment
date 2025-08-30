from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='tasks')
router.register(r'ai', views.AIViewSet, basename='ai')

urlpatterns = [
    path('', include(router.urls)),
]