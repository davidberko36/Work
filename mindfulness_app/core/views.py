from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from .serializers import UserCreateSerializer, LoginSerializer, AudioTrackSerializer, ScheduledSessionSerializer, UserSerializer
from django.contrib.auth import authenticate
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .models import AudioTrack, ScheduledSession, User, FriendRequest
from django.shortcuts import get_object_or_404

# Signup view
@api_view(['POST'])
def signup_view(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully',
                'user': UserCreateSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),


    }
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)  # This logs the user in (using Django session)

            # Get the JWT tokens
            tokens = get_tokens_for_user(user)

            return Response({
                'message': 'Login successful',
                'user': UserCreateSerializer(user).data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def refresh_access_token(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # Create a RefreshToken object
        refresh = RefreshToken(refresh_token)
        # Generate a new access token
        access = str(refresh.access_token)
        return Response({'access': access}, status=status.HTTP_200_OK)

    except TokenError as e:
        return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def audio_track_list(request):
#     if request.method == 'GET':
#         tracks = AudioTrack.objects.all()
#         serializer = AudioTrackSerializer(tracks, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = AudioTrackSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def audio_track_list(request):
    if request.method == 'GET':
        tracks = AudioTrack.objects.all()
        serializer = AudioTrackSerializer(tracks, many=True)

        # Concatenate the full Cloudinary URL for each track's audio field
        cloudinary_prefix = "https://res.cloudinary.com/dkpnqajrx/"
        for track_data in serializer.data:
            # Modify the 'audio' field to include the full URL
            track_data['audio'] = f"{cloudinary_prefix}{track_data['audio']}"

        return Response(serializer.data)

    if request.method == 'POST':
        serializer = AudioTrackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def audio_track_detail(request, pk):
    try:
        track = AudioTrack.objects.get(pk=pk)
    except AudioTrack.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AudioTrackSerializer(track)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = AudioTrackSerializer(track, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        track.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ScheduledSession Views

@api_view(['GET', 'POST'])
def session_list(request):
    if request.method == 'GET':
        sessions = ScheduledSession.objects.all()
        serializer = ScheduledSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ScheduledSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def session_detail(request, pk):
    try:
        session = ScheduledSession.objects.get(pk=pk)
    except ScheduledSession.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ScheduledSessionSerializer(session)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ScheduledSessionSerializer(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def send_friend_request(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    friend_request, created = FriendRequest.objects.get_or_create(
        sender=request.user,
        recipient=recipient
    )
    
    if not created:
        return Response({"message": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message": "Friend request sent."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def respond_to_friend_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, id=request_id, recipient=request.user)

    if action == 'accept':
        friend_request.status = 'accepted'
        friend_request.sender.add_friend(friend_request.recipient)
        friend_request.save()
        return Response({"message": "Friend request accepted."}, status=status.HTTP_200_OK)

    elif action == 'reject':
        friend_request.status = 'rejected'
        friend_request.save()
        return Response({"message": "Friend request rejected."}, status=status.HTTP_200_OK)

    return Response({"message": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def friends_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    friends = user.friends.all()
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
