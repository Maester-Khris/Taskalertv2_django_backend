from django.urls import path, include
from django.urls import path
from .views import TaskListView, TaskDetailView, TaskEditorsView, TaskAddEditorsView, TaskGroupView, TaskFilterView, TaskSearchView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list-create'),
    path('', TaskListView.as_view(), name='task-list'),
    path('<str:id>/', TaskDetailView.as_view(), name='task-detail-update'),
    path('<str:id>/editors/', TaskEditorsView.as_view(), name='task-editors'),
    path('<str:id>/editors/<str:userid>', TaskAddEditorsView.as_view(), name='task-add-editors'),
    path('bygroup', TaskGroupView.as_view(), name='task-group'),
    path('filter', TaskFilterView.as_view(), name='task-filter'),
    path('search', TaskSearchView.as_view(), name='task-search'),
]

#============ alternative 0 -recent old: with view function ==============

# urlpatterns = [
#     path('/create', views.create_task),
#     path('/list', views.list_task),
# ]


#============ alternative 1: with modelview set ==============
# from .updated_views import TaskViewSet
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register(r'tasks', TaskViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]
