# to format data i.e. python array or dicitionary to specefic format (JSON) to send to client


from rest_framework import serializers
from .models import User 

class UserSerializers(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = '__all__'