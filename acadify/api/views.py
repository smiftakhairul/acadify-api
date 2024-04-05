from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from ..models import *
from .serializers import *
from .utils import ApiUtils

@api_view(['POST'])
def register(request):
    try:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user = UserSerializer(user).data
            return ApiUtils.success_response(data={'user'}, message='User registered successfully.')
        
        return ApiUtils.error_response(message=serializer.errors)
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):
    try:
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        if user.role == request.data.get('role'):
            user = UserSerializer(user).data
            return ApiUtils.success_response(data={'user': user, 'token': token.key}, message='User authenticated successfully.')
        
        return ApiUtils.error_response(message='Invalid credentials.')
    except ValidationError as e:
        return ApiUtils.error_response(message='Invalid credentials.')
    except:
        return ApiUtils.error_response(message='Something went wrong.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
