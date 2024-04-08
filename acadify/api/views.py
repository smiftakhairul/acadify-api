from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from ..models import *
from .serializers import *
from .utils import ApiUtils, CustomPagination

@api_view(['POST'])
def register(request):
    try:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user = UserSerializer(user).data
            return ApiUtils.success_response(data={'user': user}, message='User registered successfully.')
        
        return ApiUtils.error_response(message=list(serializer.errors.values())[0][0])
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):
    try:
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        if not user.is_superuser and user.role in ['faculty', 'student']:
            user = UserSerializer(user).data
            return ApiUtils.success_response(data={'user': user, 'token': token.key}, message='User authenticated successfully.')
        
        return ApiUtils.error_response(message='Invalid credentials.')
    except ValidationError as e:
        return ApiUtils.error_response(message='Invalid credentials.')
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        request.user.auth_token.delete()
        return ApiUtils.success_response(message='User logged out successfully.')
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user(request):
    try:
        user = UserSerializer(request.user).data
        return ApiUtils.success_response(data={'user': user}, message='User retrieved successfully.')
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    try:
        serializer = UserProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = UserSerializer(request.user).data
            return ApiUtils.success_response(data={'user': user}, message='User updated successfully.')
        
        return ApiUtils.error_response(message=list(serializer.errors.values())[0][0])
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        if user.is_superuser:
            return ApiUtils.error_response(message='User not found.')
        user = UserSerializer(user).data
        return ApiUtils.success_response(data={'user': user}, message='User retrieved successfully.')
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_posts(request):
    try:
        filters = {key: value for key, value in request.GET.items() if key not in ['page_size', 'page', 'model']}
        if request.GET.get('model'):
            model = ContentType.objects.get(model=request.GET.get('model'))
            filters['model_type'] = model
        
        posts = Post.objects.filter(**filters).order_by('-id')
        
        if request.GET.get('page_size') and request.GET.get('page'):
            pagination = CustomPagination()
            paginated_posts = pagination.paginate_queryset(posts, request)
            serializer = PostSerializer(paginated_posts, many=True)
            posts = pagination.get_paginated_response(serializer.data)
        else:
            serializer = PostSerializer(posts, many=True)
            posts = serializer.data
        
        return ApiUtils.success_response(data={'posts': posts}, message='Posts retrieved successfully.')
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    try:
        if not request.data.get('model') or not request.data.get('model_id'):
            return ApiUtils.error_response(message='Model information is required.')
        
        model = ContentType.objects.get(model=request.data.get('model'))
        data = request.data.copy()
        data['model_type'] = model.pk
        
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return ApiUtils.success_response(data={'post': serializer.data}, message='Post created successfully.')
        
        return ApiUtils.error_response(message=list(serializer.errors.values())[0][0])
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if post.user != request.user:
            return ApiUtils.error_response(message='Not authorized.', code=status.HTTP_403_FORBIDDEN)
        
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ApiUtils.success_response(data={'post': serializer.data}, message='Post updated successfully.')
        
        return ApiUtils.error_response(message=list(serializer.errors.values())[0][0])
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return ApiUtils.success_response(data={'post': serializer.data}, message='Post retrieved successfully.')
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if post.user != request.user:
            return ApiUtils.error_response(message='Not authorized.', code=status.HTTP_403_FORBIDDEN)
        
        post.delete()
        return ApiUtils.success_response(message='Post deleted successfully.')
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request):
    try:
        if not request.data.get('model') or not request.data.get('model_id'):
            return ApiUtils.error_response(message='Model information is required.')
        
        model = ContentType.objects.get(model=request.data.get('model'))
        like_exists = Like.objects.filter(model_type=model.pk, model_id=request.data.get('model_id'), user=request.data.get('user')).exists()
        
        if not like_exists:
            data = request.data.copy()
            data['model_type'] = model.pk
            
            serializer = LikeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return ApiUtils.success_response(data={'like': serializer.data}, message='Liked successfully.')
            
            return ApiUtils.error_response(message=list(serializer.errors.values())[0][0])
        else:
            existing_like = Like.objects.get(model_type=model.pk, model_id=request.data.get('model_id'), user=request.data.get('user'))
            existing_like.delete()
            return ApiUtils.success_response(data=None, message='Disliked successfully.')
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    try:
        if not request.data.get('model') or not request.data.get('model_id'):
            return ApiUtils.error_response(message='Model information is required.')
        
        model = ContentType.objects.get(model=request.data.get('model'))
        data = request.data.copy()
        data['model_type'] = model.pk
        
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return ApiUtils.success_response(data={'comment': serializer.data}, message='Comment created successfully.')
        
        return ApiUtils.error_response(message=list(serializer.errors.values())[0][0])
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
        if comment.user != request.user:
            return ApiUtils.error_response(message='Not authorized.', code=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return ApiUtils.success_response(message='Comment deleted successfully.')
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
