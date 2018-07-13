from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Course, Classroom, CourseInClassroom, StudentInClassroom, StudentInCourse, Parent, Notification

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['is_professor'] = user.groups.filter(name='instructor').exists()
        token['is_parent'] = user.groups.filter(name='parent').exists()

        if token['is_professor']:
            #courses = CourseInClassroom.objects.filter(professor=user)
            courses = []
        elif token['is_parent']:
            parent = get_object_or_404(Parent, id=user.id)
            sic = StudentInClassroom.objects.filter(student__in=parent.students.all())
            memberships = StudentInCourse.objects.filter(student=sic)
            courses = [m.course for m in memberships]
        else:
            sic = StudentInClassroom.objects.filter(student=user)
            memberships = StudentInCourse.objects.filter(student=sic)
            courses = [m.course for m in memberships]
        
        notifications = Notification.objects.filter(course__in=courses)
        unread_notifications = notifications.filter(read=False)

        token['unread_notifications'] = len(unread_notifications)
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

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = Parent.objects.create(
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
        fields = ('id', 'room', 'schedule', 'created')

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
