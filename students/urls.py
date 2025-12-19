from django.urls import path
from .views import StudentListView,StudentCreateView,StudentDeleteView,StudentUpdateView,UserRegisterView,UserLogoutView,UserLoginView,ChangePasswordView,ProfileView,AdminDashboardView
urlpatterns=[
    path('',StudentListView.as_view(),name='student_list'),
    path('register/',UserRegisterView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('create/',StudentCreateView.as_view(),name='student_add'),
    path('change_password/',ChangePasswordView.as_view(),name="change_password"),
    path('profile/',ProfileView.as_view(),name="profile"),

    path('update/<int:pk>',StudentUpdateView.as_view(),name='student_update'),
    path('delete/<int:pk>',StudentDeleteView.as_view(),name='student_delete'),

  path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),

]