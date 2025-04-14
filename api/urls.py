from django.urls import path
from .views import get_all_todos

urlpatterns = [
    path('todos/', get_all_todos, name='get_all_todos'),
]

