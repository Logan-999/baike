from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, 
    UserProfileSerializer, ChangePasswordSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register(request):
    """用户注册"""
    from rest_framework.authtoken.models import Token
    
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # 创建token
        token, created = Token.objects.get_or_create(user=user)
        # 获取用户资料
        user_profile = user.profile
        return Response({
            'message': '注册成功',
            'user': UserProfileSerializer(user_profile).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def user_login(request):
    """用户登录"""
    from rest_framework.authtoken.models import Token
    
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # 获取或创建token
        token, created = Token.objects.get_or_create(user=user)
        # 获取用户资料
        user_profile = user.profile
        
        return Response({
            'message': '登录成功',
            'user': UserProfileSerializer(user_profile).data,
            'token': token.key
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """用户登出"""
    logout(request)
    return Response({'message': '登出成功'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """获取用户资料"""
    user_profile = request.user.profile
    serializer = UserProfileSerializer(user_profile)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """更新用户资料"""
    user_profile = request.user.profile
    serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': '资料更新成功', 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """修改密码"""
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        # 验证旧密码
        if not request.user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': ['旧密码错误']}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 设置新密码
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        # 更新会话认证哈希
        update_session_auth_hash(request, request.user)
        
        return Response({'message': '密码修改成功'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_auth(request):
    """检查认证状态"""
    if request.user.is_authenticated:
        user_profile = request.user.profile
        return Response({
            'is_authenticated': True,
            'user': UserProfileSerializer(user_profile).data
        })
    else:
        return Response({'is_authenticated': False})