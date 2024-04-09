from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime
from ..models import *

class BaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = naturaltime(instance.created_at)
        representation['updated_at'] = naturaltime(instance.updated_at)
        return representation

    class Meta:
        abstract = True

class UserSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = User
        exclude = ['password', 'is_superuser', 'last_name', 'is_staff']

class RegisterSerializer(BaseSerializer):
    password = serializers.CharField(write_only=True)

    class Meta(BaseSerializer.Meta):
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = User
        fields = ['first_name', 'designation', 'phone', 'avatar', 'address', 'website', 'github', 'twitter', 'facebook', 'vk', 'about']

class LikeSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Like
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation

class CommentSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Comment
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation

class AttachmentSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Attachment
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation

class PostSerializer(BaseSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    model_object = serializers.SerializerMethodField()
    
    class Meta(BaseSerializer.Meta):
        model = Post
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation
    
    def get_model_object(self, instance):
        try:
            if instance.model_type == ContentType.objects.get_for_model(Course):
                model_object = Course.objects.get(pk=instance.model_id)
                serializer = CourseSerializer(model_object)
                return serializer.data
            return None
        except:
            return None

class EnrollmentSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Enrollment
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['course'] = CourseSerializer(instance.course).data
        return representation

class CourseSerializer(BaseSerializer):
    enrollments = EnrollmentSerializer(many=True, read_only=True)
    
    class Meta(BaseSerializer.Meta):
        model = Course
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation
