# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from drf_spectacular.utils import extend_schema

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    @extend_schema(
        request=TaskSerializer,
        responses={201: TaskSerializer},
        description="Create a new task.",
        summary="Create Task",
        tags=["Tasks"],
        operation_id="createTask",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: TaskSerializer(many=True)},
        description="Retrieve a list of tasks.",
        summary="List Tasks",
        tags=["Tasks"],
        operation_id="listTasks",
    )
    def list(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    # Implement other methods (retrieve, update, destroy) similarly














# from django.http.response import JsonResponse
# from rest_framework.parsers import JSONParser 
# from rest_framework import status, viewsets
# from rest_framework.decorators import action
 
# from .models import Task
# from .serializers import TaskSerializer
# from taskmanager import utils
# from rest_framework.decorators import api_view

# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
# from drf_spectacular.types import OpenApiTypes



# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

#     @extend_schema(
#         request=TaskSerializer,
#         responses={201: TaskSerializer},
#         description="Create a new task.",
#         summary="Create Task",
#         tags=["Tasks"],
#         operation_id="createTask",
#     )
#     def create(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)

#     @extend_schema(
#         responses={200: TaskSerializer(many=True)},
#         description="Retrieve a list of tasks.",
#         summary="List Tasks",
#         tags=["Tasks"],
#         operation_id="listTasks",
#     )
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)