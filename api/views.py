from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import Message, Profile
from .serializers import MessageSerializer, SendMessageSerializer, RevealedMessageSerializer
from .permissions import IsNotBanned
import random

class SendMessageView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = SendMessageSerializer
    def perform_create(self, serializer):
        profile = self.request.user.profile
        if profile.coins < 10: return
        profile.coins -= 10
        profile.save()
        serializer.save(sender=self.request.user)

class ReceiveMessageView(APIView):
    permission_classes = [IsAuthenticated, IsNotBanned]
    def post(self, request):
        unread_messages = Message.objects.filter(receiver=None).exclude(sender=request.user)
        if not unread_messages:
            return Response("No new messages available.")
        random_message = random.choice(list(unread_messages))
        random_message.receiver = request.user
        random_message.save()
        serializer = MessageSerializer(random_message)
        return Response(serializer.data)

class RevealSenderView(APIView):
    permission_classes = [IsAuthenticated, IsNotBanned]
    def post(self, request, pk):
        profile = request.user.profile
        if profile.coins < 30:
            return Response("Not enough coins to reveal the sender.")
        message = Message.objects.get(pk=pk, receiver=request.user)
        if message.is_sender_revealed:
            return Response("Sender is already revealed.")
        profile.coins -= 30
        profile.save()
        message.is_sender_revealed = True
        message.save()
        serializer = RevealedMessageSerializer(message)
        return Response(serializer.data)

class ReplyToMessageView(APIView):
    permission_classes = [IsAuthenticated, IsNotBanned]
    def post(self, request, pk):
        profile = request.user.profile
        if profile.coins < 20:
            return Response("Not enough coins to reply.")
        message = Message.objects.get(pk=pk, receiver=request.user)
        reply_text = request.data.get('reply_text')
        if not reply_text:
            return Response("reply_text is required.")
        profile.coins -= 20
        profile.save()
        message.reply_text = reply_text
        message.save()
        serializer = RevealedMessageSerializer(message)
        return Response(serializer.data)
        
class AddFriendView(APIView):
    permission_classes = [IsAuthenticated, IsNotBanned]
    def post(self, request):
        profile = request.user.profile
        if profile.coins < 50:
            return Response("Not enough coins to add a friend.")
        friend_username = request.data.get('username')
        if not friend_username:
            return Response("Username is required.")
        friend_user = User.objects.get(username=friend_username)
        if friend_user == request.user:
            return Response("You cannot add yourself as a friend.")
        profile.friends.add(friend_user)
        profile.coins -= 50
        profile.save()
        return Response(f"{friend_username} has been added to your friends list.")

class SendMessageToFriendView(APIView):
    permission_classes = [IsAuthenticated, IsNotBanned]
    def post(self, request):
        profile = request.user.profile
        cost = 20
        if profile.coins < cost:
            return Response("Not enough coins. It costs 20 coins to message a friend and make a notification.")
        friend_username = request.data.get('receiver_username')
        text = request.data.get('text')
        friend_user = User.objects.get(username=friend_username)
        if not profile.friends.filter(pk=friend_user.pk).exists():
            return Response("This user is not in your friends list.")
        profile.coins -= cost
        profile.save()
        Message.objects.create(
            sender=request.user,
            receiver=friend_user,
            text=text,
            is_sender_revealed=True,
            is_notification=True
        )
        return Response(f"Message sent to your friend with a sexy notification {friend_username}.")

#adminstuff
class AdminMessageListView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDestroyView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Message.objects.all()

class AdminAddCoinsView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        user_id = request.data.get('user_id')
        amount = request.data.get('amount')
        if not user_id or not amount:
            return Response("user_id and amount are required.")
        user_to_update = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user_to_update)
        profile.coins += int(amount)
        profile.save()
        return Response(f"{amount} coins added to user {profile.user.username}. coin wallet: {profile.coins}")

class AdminBanUserView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"detail": "user_id is required."})
        user_to_ban = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user_to_ban)
        profile.is_banned = True
        profile.save()
        return Response(f"User {profile.user.username} has been banned.")

class AdminUnbanUserView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"detail": "user_id is required."})
        user_to_unban = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user_to_unban)
        profile.is_banned = False
        profile.save()
        return Response(f"User {profile.user.username} has been unbanned.")