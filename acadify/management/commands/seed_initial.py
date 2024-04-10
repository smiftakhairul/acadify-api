import random
from django.core.management.base import BaseCommand
from ...factories.initial_factory import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create 5 faculties
        for _ in range(5):
            FacultyFactory()

        # Create 100 students
        for _ in range(100):
            UserFactory()

        # Create posts for some users (range between 1-5)
        for user in User.objects.all():
            for _ in range(random.randint(1, 5)):
                PostFactory(user=user)

        # Create courses for faculties (range between 2-4)
        for faculty in User.objects.filter(role='faculty'):
            for _ in range(random.randint(2, 4)):
                CourseFactory(user=faculty)
                
        # Enroll some students in courses
        for course in Course.objects.all():
            available_capacity = course.capacity - course.enrollment_set.count()
            if available_capacity > 0:
                students = User.objects.filter(role='student').exclude(enrollment__course=course)
                num_students_to_enroll = min(available_capacity, 100)
                for student in students.order_by('?')[:num_students_to_enroll]:
                    EnrollmentFactory(course=course, user=student)

        self.stdout.write(self.style.SUCCESS('Data seeded successfully.'))
