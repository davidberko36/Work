from django.urls import path
from .views import signup_view, login_view, refresh_access_token, logout_view, audio_track_list, audio_track_detail, session_list, session_detail, send_friend_request, respond_to_friend_request, friends_list

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('refresh-token/', refresh_access_token, name='refresh-token'),
    path('logout/', logout_view, name='logout'),
    path('audio-tracks/', audio_track_list, name='audio_track_list'),
    path('audio-tracks/<int:pk>/', audio_track_detail, name='audio_track_detail'),
    path('sessions/', session_list, name='session_list'),
    path('sessions/<int:pk>/', session_detail, name='session_detail'),
    path('friend-requests/', send_friend_request, name='send-friend-request'),  # Send friend request
    path('friend-requests/<int:request_id>/<str:action>/', respond_to_friend_request, name='respond-to-friend-request'),
    path('friends/', friends_list, name='friends-list'),  # Get friends list
]
