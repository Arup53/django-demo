from django.urls import path
from .views import get_all_todos,create_user_with_card

urlpatterns = [
    path('todos/', get_all_todos, name='get_all_todos'),
    path('users/create-with-card/', create_user_with_card),
]

