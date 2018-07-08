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
from .models import Course, Classroom, CourseInClassroom, StudentInClassroom, StudentInCourse, Attachment, Notification, Parent
from .serializers import MyTokenObtainPairSerializer, UserSerializer, ParentSerializer, ClassroomSerializer, CourseWithProfessorSerializer
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
            serializer = ParentSerializer()
        else:
            serializer = UserSerializer()

        data = {'username':username, 'password':password2, 'email':email, 'first_name':first_name, 'last_name':last_name}
        user = serializer.create(data)

        if user_type == 'instructor' or user_type == 'parent':
            group = get_object_or_404(Group, name=user_type)
            group.user_set.add(user)
        return Response({'registered':True})

class AddStudentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        is_parent = request.user.groups.filter(name='parent').exists()
        if is_parent:
            parent = get_object_or_404(Parent, id=request.user.id)
            student_ids = [student.id for student in parent.students.all()]
            students = User.objects.exclude(groups__name='instructor').exclude(groups__name='parent').exclude(id__in=student_ids).exclude(is_superuser=True)

        s = UserSerializer(students, many=True)
        return Response(s.data)

    def post(self, request, format=None):
        print("post")
        student_username = request.data["username"]
        print("username: " + student_username)
        student = get_object_or_404(User, username=student_username)
        print(student)

        is_parent = request.user.groups.filter(name='parent').exists()

        if is_parent:
            parent = get_object_or_404(Parent, id=request.user.id)
            parent.students.add(student)
        else:
            return Response({'added':False, 'reason':'Only parents can add students'})

        return Response({'added':True})

class MineView(APIView):
    #authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsEnrolled,)

    def get(self, request, format=None):
        is_professor = request.user.groups.filter(name='instructor').exists()
        print(is_professor)
        is_parent = request.user.groups.filter(name='parent').exists()
        print(is_parent)
        
        if is_professor:
            classrooms = [c.classroom for c in CourseInClassroom.objects.filter(professor=request.user)]
        elif is_parent:
            parent = get_object_or_404(Parent, id=request.user.id)
            student_ids = [student.id for student in parent.students.all()]
            print(student_ids)
            classrooms = list(set([c.classroom for c in StudentInClassroom.objects.filter(student__in=student_ids)]))
        else:
            classrooms = [c.classroom for c in StudentInClassroom.objects.filter(student=request.user)]
            print(classrooms)

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
        is_parent = request.user.groups.filter(name='parent').exists()
        
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        courses = []
        
        if is_professor:
            courses = [c for c in CourseInClassroom.objects.filter(professor=request.user, classroom=classroom)]
        elif is_parent:
            parent = get_object_or_404(Parent, id=request.user.id)
            if StudentInClassroom.objects.filter(student__in=parent.students.all()).exists():
                courses = [c for c in CourseInClassroom.objects.filter(classroom=classroom)]
        else:
            if StudentInClassroom.objects.filter(student=request.user).exists():
                courses = [c for c in CourseInClassroom.objects.filter(classroom=classroom)]

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
        print("ClassroomEnrollView")
        print('1"')
        print("classrrom id : " + str(classroom_id))
        print("2")
        classroom = get_object_or_404(Classroom, id=classroom_id)
        print(classroom)
        if StudentInClassroom.objects.filter(student=request.user, classroom=classroom).exists():
            return Response({'enrolled':False, 'code':1, 'reason':'Already enrolled in that classoom'})
        sic = StudentInClassroom(student=request.user, classroom=classroom)
        print(sic)
        sic.save()

        for course in classroom.courses.all():
            print(course)
            cic = get_object_or_404(CourseInClassroom, course=course, classroom=classroom)
            print(cic)
            membership = StudentInCourse(student=sic, course=cic)
            print(membership)
            membership.save()

        return Response({'enrolled':True})

class StudentsAttendanceView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsEnrolled,)

    def get(self, request, classroom_id, course_id, format=None):
        print("get")
        classroom = get_object_or_404(Classroom, id=classroom_id)
        print(classroom)
        course = get_object_or_404(Course, id=course_id)
        print(course)

        #classes_done = classroom.classes_done
        is_professor = request.user.groups.filter(name='instructor').exists()
        is_parent = request.user.groups.filter(name='parent').exists()

        if is_professor:
            students = classroom.students.all()
        elif is_parent:
            parent = get_object_or_404(Parent, id=request.user.id)
            students = list(set(parent.students.all()).intersection(classroom.students.all()))
        else:
            students = classroom.students.filter(id=request.user.id)
        
        print(students)
        students_attendance = []
        
        for student in students:
            sic = get_object_or_404(StudentInClassroom, classroom=classroom, student=student)
            print(sic)
            cic = get_object_or_404(CourseInClassroom, classroom=classroom, course=course)
            print(cic)
            classes_done = cic.classes_done
            print("classes_done: " + str(classes_done))
            
            membership = get_object_or_404(StudentInCourse, student=sic, course=cic)
            print(membership)
            
            classes_attended = membership.classes_attended
            
            if classes_done is not 0:
                percentage = classes_attended / classes_done * 100
            else:
                percentage = 100
            students_attendance.append({'id':student.id,
                                        'first_name':student.first_name,
                                        'last_name':student.last_name,
                                        'percentage':"%.2f" % percentage,
                                        'classes_attended':classes_attended})
        return Response({'classes_done':classes_done, 'students':students_attendance})

    def post(self, request, classroom_id, course_id, format=None):
        students = JSONParser().parse(BytesIO(str.encode(request.data['students'])))
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        course = get_object_or_404(Course, pk=course_id)
        
        cic = get_object_or_404(CourseInClassroom, classroom=classroom, course=course)
        cic.classes_done += 1
        cic.save()
        
        for i in range(len(students)):
            is_attended = students[i]['is_attended']
            student = get_object_or_404(User, id=students[i]['id'])
            sic = get_object_or_404(StudentInClassroom, classroom=classroom, student=student)
            
            membership = get_object_or_404(StudentInCourse, student=sic, course=cic)
            
            if is_attended:
                membership.classes_attended += 1
                membership.save()
        return self.get(request, classroom_id, course_id)

class StudentsGradesView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsEnrolled,)

    def get(self, request, classroom_id, course_id, format=None):
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        course = get_object_or_404(Course, pk=course_id)
        
        is_professor = request.user.groups.filter(name='instructor').exists()
        is_parent = request.user.groups.filter(name='parent').exists()
        
        if is_professor:
            students = classroom.students.all()
        elif is_parent:
            parent = get_object_or_404(Parent, id=request.user.id)
            students = list(set(parent.students.all()).intersection(classroom.students.all()))
        else:
            students = classroom.students.filter(id=request.user.id)
        
        students_grades = []
        
        for student in students:
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
        return Response({'students':students_grades})

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

class StudentsAttachmentsView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsEnrolled,)

    def get(self, request, classroom_id, course_id, format=None):
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        course = get_object_or_404(Course, pk=course_id)
        cic = get_object_or_404(CourseInClassroom, course=course, classroom=classroom)

        attachments = Attachment.objects.filter(course=cic)
        attachment_list = []
        for attachment in attachments:
            uploader_name = attachment.uploader.first_name + ' ' + attachment.uploader.last_name
            attachment_list.append({'id':attachment.id,
                                    'file':attachment.file.name,
                                    'uploader':uploader_name,
                                    'created':attachment.created})
        return Response({'attachments':attachment_list})

    def post(self, request, classroom_id, course_id, format=None):
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        course = get_object_or_404(Course, pk=course_id)
        
        cic = get_object_or_404(CourseInClassroom, course=course, classroom=classroom)
        
        title = request.data['title']
        file =request.data['file']

        if file:
            attachment = Attachment(course=cic, uploader=request.user)
            attachment.file.save(file.name, file)
            attachment.save()

        return self.get(request, classroom_id, course_id)


class StudentsNotificationsView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsEnrolled,)

    def get(self, request, classroom_id, course_id, format=None):
        is_professor = request.user.groups.filter(name='instructor').exists()

        classroom = get_object_or_404(Classroom, pk=classroom_id)
        course = get_object_or_404(Course, pk=course_id)
        cic = get_object_or_404(CourseInClassroom, course=course, classroom=classroom)

        notifications = Notification.objects.filter(course=cic)
        notification_list = []
        
        for notification in notifications:
            author_name = notification.author.first_name + ' ' + notification.author.last_name
            notification_list.append({'id':notification.id,
                                    'subject':notification.subject,
                                    'text':notification.text,
                                    'author':author_name,
                                    'created':notification.created})
        return Response({'notifications':notification_list})

    def post(self, request, classroom_id, course_id, format=None):
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        course = get_object_or_404(Course, pk=course_id)
        
        cic = get_object_or_404(CourseInClassroom, course=course, classroom=classroom)
        subject = request.data['subject']
        text =request.data['text']

        notification = Notification(course=cic, author=request.user, subject=subject, text=text)
        notification.save()

        return self.get(request, classroom_id, course_id)
