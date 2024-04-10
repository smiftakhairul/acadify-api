import factory
from faker import Faker
from ..models import *
from ..api.utils import generate_token
import random
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        
    @classmethod
    def generate_unique_username(cls):
        while True:
            username = fake.user_name()
            if not cls._meta.model.objects.filter(username=username).exists():
                return username

    username = factory.LazyAttribute(lambda _: UserFactory.generate_unique_username())
    first_name = factory.LazyAttribute(lambda _: fake.first_name() + ' ' + fake.last_name())
    # last_name = factory.LazyAttribute(lambda _: fake.last_name())
    email = factory.LazyAttribute(lambda o: f'{o.username}@acadify.dev')
    password = make_password('password')
    role = 'student'
    phone = factory.Faker('phone_number')
    address = factory.LazyAttribute(lambda _: fake.city() + ', ' + fake.country())
    designation = factory.Faker('job')
    about = factory.Faker('text')

    @factory.post_generation
    def set_role(self, create, extracted, **kwargs):
        if extracted:
            self.role = extracted

class FacultyFactory(UserFactory):
    role = 'faculty'

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(lambda _: fake.sentence(nb_words=5))
    content = factory.LazyAttribute(lambda _: fake.paragraph())
    tags = factory.LazyAttribute(lambda _: ','.join(fake.words(nb=random.randint(1, 3))))
    model_type = factory.LazyAttribute(lambda _: ContentType.objects.get_for_model(Post))
    model_id = 0
    type = 'general'
    
    # @factory.post_generation
    # def set_model_type_and_id(self, create, extracted, **kwargs):
    #     if extracted:
    #         self.model_type = extracted
    #         if extracted == 'Post':
    #             self.model_id = 0
    #             self.type = 'general'
    #         elif extracted == 'Course':
    #             self.model_id = Course.objects.order_by('?').first().id
    #             self.type = 'general'

class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course
    
    @classmethod
    def generate_unique_token(cls):
        while True:
            token = generate_token()
            if not cls._meta.model.objects.filter(token=token).exists():
                return token

    user = factory.SubFactory(FacultyFactory)
    name = factory.LazyAttribute(lambda _: fake.sentence(nb_words=3))
    description = factory.LazyAttribute(lambda _: fake.text())
    tags = factory.LazyAttribute(lambda _: ','.join(fake.words(nb=random.randint(1, 3))))
    capacity = factory.LazyFunction(lambda: random.choice([5, 10, 15]))
    token = factory.LazyAttribute(lambda _: CourseFactory.generate_unique_token())
    status = True

class EnrollmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Enrollment

    course = factory.SubFactory(CourseFactory)
    user = factory.SubFactory(UserFactory)
    status = True
