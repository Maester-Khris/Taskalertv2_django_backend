from django.urls import path
from .views import UserListView, UserDetailView

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),  # For GET (list users) and POST (create user)
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),  # For GET (retrieve a user), PUT (update a user)
]