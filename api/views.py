from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializers

# Create your views here.
@api_view(['GET'])
def get_user(request):
      user = User.objects.all() ;
      serializer= UserSerializers(user, many=True)
      return Response(serializer.data)