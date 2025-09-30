from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=100)
    is_banned = models.BooleanField(default=False)
    friends = models.ManyToManyField(User, related_name='friend_of', blank=True)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    text = models.TextField()
    is_sender_revealed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reply_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Message from {self.sender.username}'