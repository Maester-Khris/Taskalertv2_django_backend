from django.urls import path, include
from .updated_views import TaskViewSet
from rest_framework.routers import DefaultRouter
from . import views


#============ alternative 0: with view function ==============

urlpatterns = [
    path('/create', views.create_task),
    path('/list', views.list_task),
]

#============ alternative 1: with modelview set ==============

# router = DefaultRouter()
# router.register(r'tasks', TaskViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]
