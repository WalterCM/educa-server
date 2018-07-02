from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from braces.views import LoginRequiredMixin
from classrooms.models import Classroom
from .forms import ClassroomEnrollForm


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_classroom_list')

    def form_valid(self, form):
        result = super(StudentRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result


class StudentEnrollClassroomView(LoginRequiredMixin, FormView):
    classroom = None
    form_class = ClassroomEnrollForm

    def form_valid(self, form):
        self.classroom = form.cleaned_data['classroom']
        self.classroom.students.add(self.request.user)
        return super(StudentEnrollClassroomView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_classroom_detail', args=[self.classroom.id])


class StudentClassroomListView(LoginRequiredMixin, ListView):
    model = Classroom
    template_name = 'students/classroom/list.html'

    def get_queryset(self):
        qs = super(StudentClassroomListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentClassroomDetailView(DetailView):
    model = Classroom
    template_name = 'students/classroom/detail.html'

    def get_queryset(self):
        qs = super(StudentClassroomDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentClassroomDetailView, self).get_context_data(**kwargs)
        # get classroom object
        classroom = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = classroom.modules.get(id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = classroom.modules.all()[0]
        return context
