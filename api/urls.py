from django.urls import path
from .views import *

urlpatterns = [
    
    path('messages/send/', SendMessageView.as_view(),),
    path('messages/receive/', ReceiveMessageView.as_view(),),
    path('messages/<int:pk>/reveal/', RevealSenderView.as_view(),),
    path('messages/<int:pk>/reply/', ReplyToMessageView.as_view(),),
    path('friends/add/', AddFriendView.as_view(),),
    path('friends/send-message/', SendMessageToFriendView.as_view(),),
    path('admin/messages/', AdminMessageListView.as_view(),),
    path('admin/messages/<int:pk>/delete/', MessageDestroyView.as_view(),),
    path('admin/add-coins/', AdminAddCoinsView.as_view(),),
    path('admin/ban-user/', AdminBanUserView.as_view(),),
    path('admin/unban-user/', AdminUnbanUserView.as_view(),),
]