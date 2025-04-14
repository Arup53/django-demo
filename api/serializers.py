# to format data i.e. python array or dicitionary to specefic format (JSON) to send to client


from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'