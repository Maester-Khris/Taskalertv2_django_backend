from django.urls import path, include
from django.urls import path
from .views import TaskView

urlpatterns = [
    path('', TaskView.as_view(), name='task-list'),  # For GET (list tasks) and POST (create task)
    path('<int:id>/', TaskView.as_view(), name='task-detail'),  # For GET (retrieve a task), PUT (update a task)
    path('<int:id>/editors/', TaskView.as_view(), name='task-editors'),  # For GET (retrieve editors)
    path('<int:id>/editor/<int:userid>/', TaskView.as_view(), name='task-editor'),  # For PUT (add/update editor)
    path('group/', TaskView.as_view(), name='task-group'),  # For GET (retrieve tasks by group)
    path('search/', TaskView.as_view(), name='task-search'),  # For GET (search tasks)
    path('filter/', TaskView.as_view(), name='task-filter'),  # For GET (retrieve tasks with filters)
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
