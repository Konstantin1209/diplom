from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def user_list(request):
    try:
        custom_users = CustomUser .objects.all()
        serializer = CustomUserSerializer(custom_users, many=True)
        if not serializer.data:
            return Response({"detail": "No users found."}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def user_id(request, id):
    try:
        custom_user = CustomUser.objects.get(id=id)
    except CustomUser .DoesNotExist:
        return Response({'error': 'User  not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CustomUserSerializer(custom_user)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
        




