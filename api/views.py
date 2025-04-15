from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Todo,User, CardDetails
from .serializers import TodoSerializer, CardDetailsSerializer
from .card import create_cardholder

@api_view(['GET'])
def get_all_todos(request):
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user_with_card(request):
    name = request.data.get('name')
    if not name:
        return Response({"error": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 1. Create User
        user = User.objects.create(name=name)

        # 2. Call your external card creation function
        card_obj = create_cardholder()
        
        # 3. Create CardDetails for the user
        card = CardDetails.objects.create(
            id=user.id,  # same ID as user
            user=user,
            cardholder_id=card_obj['cardholderId'],
            card_id=card_obj['cardId'],
        )

        return Response({
            "message": "success",
            "cardHolderId": card.cardholder_id,
            "cardId": card.card_id,
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)