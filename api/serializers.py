# to format data i.e. python array or dicitionary to specefic format (JSON) to send to client


from rest_framework import serializers
from .models import Todo,User, Transaction, CardDetails


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'



class CardDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDetails
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    carddetails = CardDetailsSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'