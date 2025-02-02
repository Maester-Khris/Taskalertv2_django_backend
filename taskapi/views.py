from django.shortcuts import render

from django.http.response import JsonResponse

from rest_framework import status, viewsets, serializers
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework.decorators import api_view, action

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
 
from .models import Task
from .serializers import TaskSerializer
from taskmanager import utils



class InputSerializer(serializers.Serializer): 
    name= serializers.CharField(),
    description= serializers.CharField(),
    group= serializers.CharField()

@extend_schema(
    request=InputSerializer,
    description='This api method provide an endpoint to create a task',
    auth=None,
    operation_id=None,
    operation=None,
    examples=[
        OpenApiExample(
            'New task creation: Dev project',
            description='This is the list of task defined for our dev project',
            value="{name: 'creation of repository', description: 'push of exixting files', group:'work'}"
        )
    ]
)
@api_view(['POST'])
def create_task(request):
    print("================== my data ====================")
    print(request.data) #able to retrieve data
    # task_data = JSONParser().parse(request)
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#==============================================================================================

@extend_schema(
    description='This api method provide an endpoint to list all the task present in the collections',
    auth=None,
    operation_id=None,
    operation=None,
    examples=[
        OpenApiExample(
            'Task List',
            description='This is the list of task defined for our dev project',
            value="[{id:1, name:'Dev project', group:'work', description:'this is where the magic happens'}, {id:2, name:'Investment project', group:'Finance', description:'this is where the money grow'}]"
        )
    ]
)
@api_view(['GET'])
def list_task(request):
    pizza = utils.listTask()
    serializer = TaskSerializer(pizza, many=True)
    return JsonResponse(serializer.data, safe=False)
    

#@action(detail=True, methods=['get'])