
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
 
from .models import Task
from .serializers import TaskSerializer
from userapi.serializers import UserSerializer
from userapi.models import User
from taskmanager import utils



class TaskGroupSerializer(serializers.Serializer):
    groups = serializers.ListField()


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
        description="Retrieve a task by ID."
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
        description="Update a task by ID."
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
        #request=UserSerializer,
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
                # If user is already an editor, update can be handled here if needed
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
        responses={200: TaskSerializer(many=True)},
        description="Retrieve tasks with title filter and result paginated."
    )
    def get(self, request):
        title = request.query_params.get('title', None)
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        tasks = Task.objects.filter(title__icontains=title)
       
        # Pagination logic (basic example)
        start = (int(page) - 1) * int(limit)
        end = start + int(limit)
        tasks = tasks[start:end]

        #page_nb = 2 
        # items_per_page = 10 
        # offset = (page_nb - 1) * items_per_page
        # list = Books.objects.skip( offset ).limit( items_per_page )

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskSearchView(APIView):
    @extend_schema(
        responses={200: TaskSerializer(many=True)},
        description="Search tasks by a query string."
    )
    def get(self, request):
        query = request.query_params.get('query', '')
        tasks = Task.objects.filter(title__icontains=query) | Task.objects.filter(description__icontains=query)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


# class TaskView(APIView):
#     @extend_schema(
#         request=TaskSerializer,
#         responses={201: TaskSerializer, 400: 'Bad Request'},
#         description="Create a new task."
#     )
#     def post(self, request):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             task = serializer.save()
#             return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @extend_schema(
#         responses={200: TaskSerializer(many=True)},
#         description="Retrieve a list of tasks."
#     )
#     def get(self, request):
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)

#     @extend_schema(
#         responses={200: TaskSerializer, 404: 'Not Found'},
#         description="Retrieve a task by ID."
#     )
#     def get_task(self, request, id):
#         try:
#             task = Task.objects.get(id=id)
#             serializer = TaskSerializer(task)
#             return Response(serializer.data)
#         except Task.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     @extend_schema(
#         request=TaskSerializer,
#         responses={200: TaskSerializer, 400: 'Bad Request', 404: 'Not Found'},
#         description="Update a task by ID."
#     )
#     def put(self, request, id):
#         try:
#             task = Task.objects.get(id=id)
#             serializer = TaskSerializer(task, data=request.data)
#             if serializer.is_valid():
#                 updated_task = serializer.save()
#                 return Response(TaskSerializer(updated_task).data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Task.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     @extend_schema(
#         responses={200: UserSerializer(many=True), 404: 'Not Found'},
#         description="Retrieve a list of editors for a specific task."
#     )
#     def get_editors(self, request, id):
#         try:
#             task = Task.objects.get(id=id)
#             editors = task.editors
#             serializer = UserSerializer(editors, many=True)
#             return Response(serializer.data)
#         except Task.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     @extend_schema(
#         request=UserSerializer,
#         responses={200: TaskSerializer, 400: 'Bad Request', 404: 'Not Found'},
#         description="Add or update an editor for a specific task."
#     )
#     def put_editor(self, request, id, userid):
#         try:
#             task = Task.objects.get(id=id)
#             user = User.objects.get(id=userid)

#             if user not in task.editors:
#                 task.editors.append(user)
#             else:
#                 # If user is already an editor, update can be handled here if needed
#                 pass
            
#             task.save()
#             return Response(TaskSerializer(task).data)
#         except (Task.DoesNotExist, User.DoesNotExist):
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     @extend_schema(
#         responses={200: TaskSerializer(many=True)},
#         description="Retrieve tasks by group name."
#     )
#     def get_tasks_by_group(self, request):
#         group_name = request.query_params.get('name')
#         tasks = Task.objects.filter(group=group_name)
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)

#     @extend_schema(
#         responses={200: TaskSerializer(many=True)},
#         description="Retrieve tasks with optional filters."
#     )
#     def get_filtered_tasks(self, request):
#         title = request.query_params.get('title', None)
#         description = request.query_params.get('description', None)
#         item = request.query_params.get('item', None)
#         page = request.query_params.get('page', 1)
#         limit = request.query_params.get('limit', 10)

#         tasks = Task.objects.all()

#         if title:
#             tasks = tasks.filter(title__icontains=title)
#         if description:
#             tasks = tasks.filter(description__icontains=description)
#         if item:
#             tasks = tasks.filter(items__name__icontains=item)

#         # Pagination logic (basic example)
#         start = (int(page) - 1) * int(limit)
#         end = start + int(limit)
#         tasks = tasks[start:end]

#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)

#     @extend_schema(
#         responses={200: TaskSerializer(many=True)},
#         description="Search tasks by a query string."
#     )
#     def search_tasks(self, request):
#         query = request.query_params.get('query', '')
#         tasks = Task.objects.filter(title__icontains=query) | Task.objects.filter(description__icontains=query)
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)
   



# ============= recent old ====================
# class InputSerializer(serializers.Serializer): 
#     name= serializers.CharField(),
#     description= serializers.CharField(),
#     group= serializers.CharField()

# @extend_schema(
#     request=InputSerializer,
#     description='This api method provide an endpoint to create a task',
#     auth=None,
#     operation_id=None,
#     operation=None,
#     examples=[
#         OpenApiExample(
#             'New task creation: Dev project',
#             description='This is the list of task defined for our dev project',
#             value="{name: 'creation of repository', description: 'push of exixting files', group:'work'}"
#         )
#     ]
# )
# @api_view(['POST'])
# def create_task(request):
#     print("================== my data ====================")
#     print(request.data) #able to retrieve data
#     # task_data = JSONParser().parse(request)
#     serializer = TaskSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED) 
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #==============================================================================================

# @extend_schema(
#     description='This api method provide an endpoint to list all the task present in the collections',
#     auth=None,
#     operation_id=None,
#     operation=None,
#     examples=[
#         OpenApiExample(
#             'Task List',
#             description='This is the list of task defined for our dev project',
#             value="[{id:1, name:'Dev project', group:'work', description:'this is where the magic happens'}, {id:2, name:'Investment project', group:'Finance', description:'this is where the money grow'}]"
#         )
#     ]
# )
# @api_view(['GET'])
# def list_task(request):
#     pizza = utils.listTask()
#     serializer = TaskSerializer(pizza, many=True)
#     return JsonResponse(serializer.data, safe=False)
    


# ============= more old ====================
#@action(detail=True, methods=['get'])