from rest_framework.response import Response
from rest_framework import status

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
