from rest_framework.serializers import ModelSerializer
from .models import Message, User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class SendMessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ('text',)

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class RevealedMessageSerializer(ModelSerializer):
    sender = UserSerializer()
    class Meta:
        model = Message
        fields = '__all__'