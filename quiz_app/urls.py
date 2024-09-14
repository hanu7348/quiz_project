# quiz_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user/subject/<int:subject_id>/quizzes/', views.quiz_list, name='quiz_list'),
    path('user/quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('user/quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('user/quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    path('user/profile/', views.profile, name='profile'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/quiz/create/', views.create_quiz, name='create_quiz'),
    path('admin/quiz/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]