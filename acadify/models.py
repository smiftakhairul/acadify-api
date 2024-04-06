from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .api.utils import UploadUtils

class User(AbstractUser):
    ROLES = (('admin', 'Admin'), ('faculty', 'Faculty'), ('student', 'Student'))
    role = models.CharField(max_length=10, choices=ROLES, default='student')
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(max_length=255, upload_to=UploadUtils.avatar, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    vk = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    model_id = models.PositiveIntegerField()
    model_object = GenericForeignKey('model_type', 'model_id')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['model_type']),
            models.Index(fields=['model_type', 'model_id']),
            models.Index(fields=['model_type', 'model_id', 'user']),
        ]

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    model_id = models.PositiveIntegerField()
    model_object = GenericForeignKey('model_type', 'model_id')
    content = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['model_type']),
            models.Index(fields=['model_type', 'model_id']),
            models.Index(fields=['model_type', 'model_id', 'user']),
        ]
        
class Attachment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    model_id = models.PositiveIntegerField()
    model_object = GenericForeignKey('model_type', 'model_id')
    attachment = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['model_type']),
            models.Index(fields=['model_type', 'model_id']),
            models.Index(fields=['model_type', 'model_id', 'user']),
        ]

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    image = models.ImageField(max_length=255, upload_to=UploadUtils.post, null=True, blank=True)
    title = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    is_announcement = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['type', 'user']),
        ]
    
    def likes(self):
        return Like.objects.filter(model_type=ContentType.objects.get_for_model(self), model_id=self.id)
    
    def comments(self):
        return Comment.objects.filter(model_type=ContentType.objects.get_for_model(self), model_id=self.id)
    
    def attachments(self):
        return Attachment.objects.filter(model_type=ContentType.objects.get_for_model(self), model_id=self.id)

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    capacity = models.PositiveIntegerField(default=1)
    tags = models.CharField(max_length=255, null=True, blank=True)
    gc_attendance = models.FloatField(default=5)
    gc_assignment = models.FloatField(default=10)
    gc_quiz = models.FloatField(default=20)
    gc_midterm = models.FloatField(default=25)
    gc_final = models.FloatField(default=40)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['user']),
            models.Index(fields=['course', 'user']),
        ]
        unique_together = ('course', 'user')

class Grade(models.Model):
    GC_TYPES = (('attendance', 'Attendance'), ('assignment', 'Assignment'), ('quiz', 'Quiz'), ('midterm', 'Midterm'), ('final', 'Final'))
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    gc_type = models.CharField(max_length=20, choices=GC_TYPES)
    total_marks = models.FloatField()
    obtained_marks = models.FloatField()
    obtained_percentage = models.FloatField()
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['enrollment']),
            models.Index(fields=['enrollment', 'gc_type']),
        ]
