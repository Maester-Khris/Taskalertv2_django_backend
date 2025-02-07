from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from drf_spectacular.utils import extend_schema

class UserListView(APIView):
    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer, 400: 'Bad Request'},
        description="Create a new user."
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: UserSerializer(many=True)},
        description="Retrieve a list of users."
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    @extend_schema(
        responses={200: UserSerializer, 404: 'Not Found'},
        description="Retrieve a user by ID."
    )
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer, 400: 'Bad Request', 404: 'Not Found'},
        description="Update a user by ID."
    )
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# class UserView(APIView):

#     @extend_schema(
#         request=UserSerializer,
#         responses={201: UserSerializer, 400: 'Bad Request'},
#         description="Create a new user."
#     )
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @extend_schema(
#         responses={200: UserSerializer(many=True)},
#         description="Retrieve a list of users."
#     )
#     def get(self, request):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

#     @extend_schema(
#         responses={200: UserSerializer, 404: 'Not Found'},
#         description="Retrieve a user by ID."
#     )
#     def get_user(self, request, id):
#         try:
#             user = User.objects.get(id=id)
#             serializer = UserSerializer(user)
#             return Response(serializer.data)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     @extend_schema(
#         request=UserSerializer,
#         responses={200: UserSerializer, 400: 'Bad Request', 404: 'Not Found'},
#         description="Update a user by ID."
#     )
#     def put(self, request, id):
#         try:
#             user = User.objects.get(id=id)
#             serializer = UserSerializer(user, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

  
