from django.shortcuts import render
from django.conf import settings
from pymongo.mongo_client import MongoClient
from bson import ObjectId

from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
 
from .models import Task
from userapi.models import User
from .serializers import TaskSerializer
from userapi.serializers import UserSerializer


class FilterSerializer(serializers.Serializer):
    totalTasks = serializers.IntegerField()
    totalPages = serializers.IntegerField()
    currentPage = serializers.IntegerField()
    tasks = TaskSerializer(many=True)


class TaskListView(APIView):
    @extend_schema(
        responses={200: TaskSerializer(many=True)},
        description="Retrieve a list of tasks."
    )
    def get(self, request):
        tasks = Task.objects.all()
        print("===========display==========")
        print(tasks)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=TaskSerializer,
        responses={201: TaskSerializer, 400: 'Bad Request'},
        description="Create a new task."
    )
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TaskDetailView(APIView):
    @extend_schema(
        responses={200: TaskSerializer, 404: 'Not Found'},
        description="Retrieve a task by object ID."
    )
    def get(self, request, id):
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=TaskSerializer,
        responses={200: TaskSerializer, 400: 'Bad Request', 404: 'Not Found'},
        description="Update a task By Object ID."
    )
    def put(self, request, id):
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                updated_task = serializer.save()
                return Response(TaskSerializer(updated_task).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class TaskEditorsView(APIView):
    @extend_schema(
        responses={200: UserSerializer(many=True), 404: 'Not Found'},
        description="Retrieve a list of editors for a specific task."
    )
    def get(self, request, id):
        try:
            task = Task.objects.get(id=id)
            editors = task.editors
            serializer = UserSerializer(editors, many=True)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

   

class TaskAddEditorsView(APIView):
    @extend_schema(
        responses={200: TaskSerializer, 400: 'Bad Request', 404: 'Not Found'},
        description="Add or update an editor for a specific task."
    )
    def put(self, request, id, userid):
        try:
            task = Task.objects.get(id=id)
            user = User.objects.get(id=userid)

            if user not in task.editors:
                task.editors.append(user)
            else:
                pass
            
            task.save()
            return Response(TaskSerializer(task).data)
        except (Task.DoesNotExist, User.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)



class TaskGroupView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter('group', str, description='group name', required=True), 
        ],
        responses={200: TaskSerializer(many=True)},
        description="Retrieve tasks by group name."
    )
    def get(self, request):
        group_name = request.query_params.get('group')
        tasks = Task.objects(group__in=[group_name])
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)



class TaskFilterView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter('title', str, description='filter by title', required=True), 
            OpenApiParameter('page', str, description='result page to return', required=False), 
            OpenApiParameter('limit', str, description='maximum results per page', required=False), 
        ],
        responses={200: FilterSerializer()},
        description="Retrieve tasks with title filter and result paginated."
    )
    def get(self, request):
        title = request.query_params.get('title', None)
        print(title)
        page = int(request.query_params.get('page', 1))
        itemlimit = int(request.query_params.get('limit', 10))

        total_items = Task.objects.filter(title__icontains=title).count()
        if page>1 :
            offset = (page - 1) * itemlimit
            tasks = Task.objects.filter(title__icontains=title).skip( offset ).limit( itemlimit )
        else:
            tasks = Task.objects.filter(title__icontains=title).limit( itemlimit )
        
        data = {
            "totalTasks": total_items,
            "totalPages": (total_items + itemlimit - 1) // itemlimit,
            "currentPage": page,
            "tasks": tasks  # This should be a list of serialized tasks
        }
        task_serializer = TaskSerializer(tasks, many=True)
        response_data = {
            "totalTasks": data["totalTasks"],
            "totalPages": data["totalPages"],
            "currentPage": data["currentPage"],
            "tasks": task_serializer.data
        }

        serializer = FilterSerializer(response_data)
        return Response(serializer.data)



class TaskSearchView(APIView):
    client = MongoClient(settings.MONGO_CONNECTION_URI)
    tasksdatabase = client[settings.MONGO_DATABASE_NAME]
    taskcollection = tasksdatabase[settings.MONGO_COLLECTION_NAME]
    
    @extend_schema(
        parameters=[
            OpenApiParameter('query', str, description='text data to search', required=True), 
        ],
        responses={200: TaskSerializer(many=True)},
        description="Search tasks by a query string."
    )
    def get(self, request):
        query = request.query_params.get('query', '')
        search_query = {
            "$search": {
                "index": "tasks-ft-search",  
                "compound": {
                    "should": [
                        {
                            "text": {
                                "query": query,
                                "path": "title",
                                "fuzzy": {}
                            }
                        },
                        {
                            "text": {
                                "query": query,
                                "path": "description",
                                "fuzzy": {}
                            }
                        },
                        {
                            "text": {
                                "query": query,
                                "path": "items",
                                "fuzzy": {}
                            }
                        }
                    ]
                }
            }
        }

        # Run the search query
        results = list(self.taskcollection.aggregate([
            search_query,
             {
                "$lookup": {
                    "from": "users",  # The name of your user collection
                    "localField": "editors",  # Field in the task document
                    "foreignField": "_id",  # The field in the user document
                    "as": "editor_details"  # Name for the output array
                }
            },
            {
                "$project": {
                    "title": 1,
                    "group": 1,
                    "description": 1,
                    "items": 1,
                    "editors": "$editor_details",  # Use the resolved user details
                    "created_at": 1
                }
            }
        ]))
        serializer = TaskSerializer(results, many=True)
        return Response(serializer.data)

