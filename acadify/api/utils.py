from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
from math import ceil
import random, string

def custom_exception_handler(exc, context):
    if isinstance(exc, AuthenticationFailed):
        return ApiUtils.error_response(message='Invalid token.', code=status.HTTP_401_UNAUTHORIZED)
    
    return None
class ApiUtils:
    @staticmethod
    def success_response(data=None, message=None, code=status.HTTP_200_OK):
        return Response({
            'status': 'success',
            'message': message,
            'data': data,
            'code': code
        }, status=code)
    
    @staticmethod
    def error_response(message=None, code=status.HTTP_400_BAD_REQUEST):
        return Response({
            'status': 'error',
            'message': message,
            'data': None,
            'code': code
        }, status=code)

    @staticmethod
    def not_found(message='Resource not found', code=status.HTTP_404_NOT_FOUND):
        return ApiUtils.error_response(message, code)

    @staticmethod
    def unauthorized(message='Unauthorized', code=status.HTTP_401_UNAUTHORIZED):
        return ApiUtils.error_response(message, code)

    @staticmethod
    def handle_exception(exception):
        return ApiUtils.error_response('Something went wrong. Please try again.', status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomPagination(PageNumberPagination):
    def get_page_size(self, request):
        page_size = request.query_params.get('page_size', 10)
        if page_size and page_size.isdigit():
            return int(page_size)
        return super().get_page_size(request)

    def paginate_queryset(self, queryset, request, view=None):
        self.total_items = len(queryset)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        total_pages = ceil(self.total_items / self.get_page_size(self.request))
        current_page = self.page.number if self.page else None
        
        return {
            'total_pages': total_pages,
            'current_page': current_page,
            'count': self.total_items,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        }

class UploadUtils:
    @staticmethod
    def avatar(instance, filename):
        name, extension = filename.split('.')
        new_filename = f"{instance.username}.{extension}"
        return f"avatars/{new_filename}"
    
    @staticmethod
    def post(instance, filename):
        name, extension = filename.split('.')
        new_filename = f"{int(timezone.now().timestamp())}.{extension}"
        return f"posts/{new_filename}"
    
    @staticmethod
    def course(instance, filename):
        name, extension = filename.split('.')
        new_filename = f"{int(timezone.now().timestamp())}.{extension}"
        return f"courses/{new_filename}"

def generate_token(size=20):
    characters = string.ascii_lowercase + string.digits + '!@#$%^&*()_+=-'
    return ''.join(random.choice(characters) for _ in range(size))
