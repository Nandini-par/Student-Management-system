from django.shortcuts import render,redirect,get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from .models import Student
from .forms import StudentForm
from .mixins import StaffRequiredMixin, AdminOnlyMixin, ReadOnlyMixin



class UserRegisterView(CreateView):
    model = User
    fields = ['username', 'password']
    template_name = 'students/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, "Congratulations! User has been created.")
        return super().form_valid(form)


class UserLoginView(TemplateView):
    template_name = 'students/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_list')
        messages.error(request, "Please enter valid credentials")
        return render(request, self.template_name)


class UserLogoutView(LoginRequiredMixin, TemplateView):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')




class StudentListView(ReadOnlyMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        sort_by = self.request.GET.get('sort_by', 'name')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(email__icontains=query)
            )
        if sort_by == 'age':
            queryset = queryset.order_by('age')
        else:
            queryset = queryset.order_by('name')
        return queryset


class StudentCreateView(StaffRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        student = form.save(commit=False)
        student.created_by = self.request.user
        student.save()
        form.save_m2m()  
        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def dispatch(self, request, *args, **kwargs):
        student = self.get_object()
        if (
            student.created_by != request.user
            and not request.user.is_staff
            and not request.user.has_perm('students.can_update_student')
        ):
            return HttpResponseForbidden("You cannot update this student")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save_m2m()  
        return response


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')

    def dispatch(self, request, *args, **kwargs):
        student = self.get_object()

        if student.created_by != request.user and not request.user.is_staff:
            return HttpResponseForbidden("You cannot delete this student")

        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'students/profile.html'


class ChangePasswordView(PasswordChangeView):
    template_name = 'students/password_change_form.html'
    success_url = reverse_lazy('student_list')

class AdminDashboardView(AdminOnlyMixin, TemplateView):
    template_name = 'students/admin_dashboard.html'
