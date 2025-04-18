from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Todo,User, CardDetails, Transaction
from .serializers import TodoSerializer, CardDetailsSerializer
from .card import create_cardholder, accept_policy, pay_with_virtual_card

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
    


@api_view(['PUT'])
def approve_card(request):
    cardholder_id = request.data.get('cardHolderId')
    card_id = request.data.get('cardId')

    if not cardholder_id or not card_id:
        return Response({"error": "cardHolderId and cardId are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 1. Call external update function (policy + activation)
        accept_policy(cardholder_id, card_id)

        # 2. Update CardDetails status in DB
        card = CardDetails.objects.get(card_id=card_id)
        card.status = True
        card.save()

        return Response({"message": "success"}, status=status.HTTP_200_OK)

    except CardDetails.DoesNotExist:
        return Response({"error": "Card not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
def create_transaction(request):
    user_id = request.data.get('userId')
    card_id = request.data.get('cardId')
    amount = request.data.get('amount')

    if not user_id or not card_id or not amount:
        return Response({"error": "userId, cardId, and amount are required."}, status=status.HTTP_400_BAD_REQUEST)

    # 1. Try to make payment with virtual card
    payment_result = pay_with_virtual_card(card_id, amount)  # Stripe uses cents

    if payment_result.get("approved"):
        try:
            user = User.objects.get(id=user_id)
            transaction = Transaction.objects.create(user=user, amount=amount)
            return Response({
                "message": "success",
                "amount": transaction.amount
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Database error", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"message": "Transaction declined"}, status=status.HTTP_402_PAYMENT_REQUIRED)