import json
from io import BytesIO
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Course, Classroom, CourseInClassroom, StudentInClassroom, StudentInCourse, Notification
from .serializers import MyTokenObtainPairSerializer, UserSerializer, ClassroomSerializer, CourseWithProfessorSerializer
from .permissions import IsEnrolled

# User auth and management

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenObtainPairSerializer

class UserRegisterView(APIView):
    #authentication_classes = 
    permission_classes = [AllowAny,]

    def post(self, request, format=None):
        username = request.data['username']

        if username is '':
            return Response({'registered':False, 'reason':'username must not be empty'})

        if User.objects.filter(username=username).exists():
            return Response({"registered":False, 'reason':'username must be unique'})

        password1 = request.data['password1']
        password2 = request.data['password2']

        if password1 != password2:
            return Response({'registered':False, 'reason':'passwords are not the same'})

        email = request.data['email']
        first_name = request.data['first_name']
        last_name = request.data['last_name']

        user_type = request.data['user_type']
        if user_type == 'parent':
            pass
        else:
            serializer = UserSerializer()

        data = {'username':username, 'password':password2, 'email':email, 'first_name':first_name, 'last_name':last_name}

        user = serializer.create(data)
        user_type = request.data['user_type']

        if user_type == 'instructor':
            instructor = get_object_or_404(Group, name=user_type)
            instructor.user_set.add(user)
        return Response({'registered':True})


# class CourseListView(generics.ListAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

# class CourseDetailView(generics.RetrieveAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

# class MineView(APIView):
#     #authentication_classes = (JWTAuthentication,)
#     permission_classes = (IsAuthenticated, IsEnrolled,)

#     def get(self, request, format=None):
#         is_professor = request.user.groups.filter(name='instructor').exists()
#         if is_professor:
#             courses = [c for c in CourseInClassroom.objects.filter(professor=request.user)]
#         elif StudentInClassroom.objects.filter(student=request.user).exists():
#             classroom = StudentInClassroom.objects.filter(student=request.user)[0].classroom
#             courses = [c for c in CourseInClassroom.objects.filter(classroom=classroom)]
#         else:
#             courses = []

#         s = CourseWithProfessorSerializer(courses, many=True)
#         return Response(s.data)

class MineView(APIView):
    #authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsEnrolled,)

    def get(self, request, format=None):
        is_professor = request.user.groups.filter(name='instructor').exists()
        if is_professor:
            classrooms = [c.classroom for c in CourseInClassroom.objects.filter(professor=request.user)]
        else:
            classrooms = [c.classroom for c in StudentInClassroom.objects.filter(student=request.user)]


        s = ClassroomSerializer(classrooms, many=True)
        return Response(s.data)

class NotmineView(APIView):
    def get(self, request, format=None):
        is_professor = request.user.groups.filter(name='instructor').exists()
        if is_professor:
            classrooms = []
            return Response({"enrollment":False, "reason":"Professors shouldn't be able to enroll"})
        else:
            if StudentInClassroom.objects.filter(student=request.user).exists():
                classrooms = []
            else:
                classrooms = Classroom.objects.all()


        s = ClassroomSerializer(classrooms, many=True)
        return Response(s.data)
        
class CoursesFromClassroomView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsEnrolled,)

    def get(self, request, classroom_id, format=None):
        is_professor = request.user.groups.filter(name='instructor').exists()
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        if is_professor:
            courses = [c for c in CourseInClassroom.objects.filter(professor=request.user, classroom=classroom)]
        elif StudentInClassroom.objects.filter(student=request.user).exists():
            courses = [c for c in CourseInClassroom.objects.filter(classroom=classroom)]
        else:
            courses = []

        s = CourseWithProfessorSerializer(courses, many=True)
        return Response(s.data)


# class ClassroomCreateView(APIView):
#     authentication_classes = (JWTAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, format=None):
#         print("ClassroomCreateView")
#         room = request.data['room']
#         if Classroom.objects.filter(room=room).exists():
#             return Response({'created':False, 'reason':'The room already exists'})

#         course_title = request.data['course']
#         course = Course.objects.filter(title=course_title)[0]
#         new_classroom = Classroom(professor=request.user, course=course, room=room, slug=room.lower())
#         new_classroom.save()
#         return Response({'created':True})

class ClassroomEnrollView(APIView):
    def post(self, request, classroom_id, format=None):
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        if StudentInClassroom.objects.filter(student=request.user, classroom=classroom).exists():
            return Response({'enrolled':False, 'code':1, 'reason':'Already enrolled in that classoom'})
        s = StudentInClassroom(student=request.user, classroom=classroom)
        s.save()
        #classroom.students.add(request.user)
        return Response({'enrolled':True})

class StudentsAttendanceView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsEnrolled,)

    def get(self, request, classroom_id, format=None):
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        classes_done = classroom.classes_done
        is_professor = request.user.groups.filter(name='instructor').exists()
        if is_professor:
            students = classroom.students.all()
        else:
            students = classroom.students.filter(id=request.user.id)

        students_attendance = []
        for i in range(len(students)):
            student = students[i]
            studentInClassroom = get_object_or_404(StudentInClassroom, classroom=classroom, student=student)
            if classes_done is not 0:
                percentage = studentInClassroom.classes_attended / classes_done * 100
            else:
                percentage = 100
            students_attendance.append({'id':student.id,
                                        'first_name':student.first_name,
                                        'last_name':student.last_name,
                                        'percentage':"%.2f" % percentage,
                                        'classes_attended':studentInClassroom.classes_attended})
        return Response({'is_professor':is_professor, 'classes_done':classes_done, 'students':students_attendance})

    def post(self, request, classroom_id, format=None):
        students = JSONParser().parse(BytesIO(str.encode(request.data['students'])))
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        classroom.classes_done += 1
        classroom.save()
        for i in range(len(students)):
            is_attended = students[i]['is_attended']
            print(is_attended)
            student = get_object_or_404(User, id=students[i]['id'])
            studentInClassroom = get_object_or_404(StudentInClassroom, classroom=classroom, student=student)
            if is_attended:
                studentInClassroom.classes_attended += 1
            studentInClassroom.save()
        return self.get(request, classroom_id)

class StudentsGradesView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsEnrolled,)

    def get(self, request, classroom_id, course_id, format=None):
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        course = get_object_or_404(Course, pk=course_id)
        is_professor = request.user.groups.filter(name='instructor').exists()
        if is_professor:
            students = classroom.students.all()
        else:
            students = classroom.students.filter(id=request.user.id)
        students_grades = []
        for i in range(len(students)):
            student = students[i]
            sic = get_object_or_404(StudentInClassroom, classroom=classroom, student=student)
            cic = get_object_or_404(CourseInClassroom, classroom=classroom, course=course)
            membership = get_object_or_404(StudentInCourse, student=sic, course=cic)
            pc_average = (membership.pc1 + membership.pc2 + membership.pc3 + membership.pc4) / 4
            grade_average = (3 * pc_average + 3 * membership.midterm + 4 * membership.final) / 10
            students_grades.append({'id':student.id,
                                    'first_name':student.first_name,
                                    'last_name':student.last_name,
                                    'pc1':membership.pc1,
                                    'pc2':membership.pc2,
                                    'pc3':membership.pc3,
                                    'pc4':membership.pc4,
                                    'midterm':membership.midterm,
                                    'final':membership.final,
                                    'pc_average':"%.2f" % pc_average,
                                    'grade_average':"%.2f" % grade_average})
        return Response({'is_professor':is_professor, 'students':students_grades})

    def post(self, request, classroom_id, course_id, format=None):
        students = JSONParser().parse(BytesIO(str.encode(request.data['students'])))
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        course = get_object_or_404(Course, pk=course_id)
        for i in range(len(students)):
            student = get_object_or_404(User, id=students[i]['id'])

            sic = get_object_or_404(StudentInClassroom, classroom=classroom, student=student)
            cic = get_object_or_404(CourseInClassroom, classroom=classroom, course=course)
            membership = get_object_or_404(StudentInCourse, student=sic, course=cic)

            membership.pc1 = students[i]['pc1']
            membership.pc2 = students[i]['pc2']
            membership.pc3 = students[i]['pc3']
            membership.pc4 = students[i]['pc4']
            membership.midterm = students[i]['midterm']
            membership.final = students[i]['final']
            membership.save()

        return self.get(request, classroom_id, course_id)

class StudentsNotificationsView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsEnrolled,)

    def get(self, request, classroom_id, course_id, format=None):
        is_professor = request.user.groups.filter(name='instructor').exists()

        classroom = get_object_or_404(Classroom, pk=classroom_id)
        print(classroom)
        print()
        course = get_object_or_404(Course, pk=course_id)
        print(course)
        print()
        cic = get_object_or_404(CourseInClassroom, course=course, classroom=classroom)
        print(cic)
        print()

        print("before trying to get notifications")
        notifications = Notification.objects.filter(course=cic)
        print("after trying to get notifications")
        print(notifications)
        notification_list = []
        for i in range(len(notifications)):
            notification = notifications[i]
            print(notification)
            print(notification.author)
            author_name = notification.author.first_name + ' ' + notification.author.last_name
            print('author_name: ' + author_name)
            notification_list.append({'id':notification.id,
                                    'subject':notification.subject,
                                    'text':notification.text,
                                    'author':author_name,
                                    'created':notification.created})
        return Response({'is_professor':is_professor, 'notifications':notification_list})

    def post(self, request, classroom_id, course_id, format=None):
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        course = get_object_or_404(Course, pk=course_id)
        cic = get_object_or_404(CourseInClassroom, course=course, classroom=classroom)
        subject = request.data['subject']
        text =request.data['text']

        notification = Notification(course=cic, author=request.user, subject=subject, text=text)
        notification.save()

        return self.get(request, classroom_id, course_id)
