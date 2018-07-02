from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Course, Classroom, CourseInClassroom, StudentInClassroom, StudentInCourse

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['is_professor'] = user.groups.filter(name='instructor').exists()
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'overview', 'image')

class CourseWithProfessorSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=False)
    professor = ProfessorSerializer(many=False)
    class Meta:
        model = CourseInClassroom
        fields = ('course', 'professor')

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ('id', 'room', 'created', 'classes_done')

# class ClassroomWithStudentsSerializer(serializers.ModelSerializer):
#     classroom = ClassroomSerializer(many=False)
#     students = UserSerializer(many=True)
#     class Meta:
#         model = StudentInClassroom
#         fields = ('classroom', 'students')

# class ClassroomWithCoursesSerializer(serializers.ModelSerializer):
#     classroom = ClassroomSerializer(many=False)
#     courses = CourseSerializer(many=True)
#     class Meta:
#         model = CourseInClassroom
#         fields = ('classroom', 'courses')

# class NotificacionSerializer(serializers.ModelSerializer):
#     classroom = ClassroomSerializer(many=False)
#     class Meta:
#         model = Notification
#         fields = {'classroom', 'subject', 'text'}