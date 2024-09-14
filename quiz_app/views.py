# quiz_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Avg
from .models import Subject, Quiz, Question, Choice, QuizResult, QuizAttempt
from .forms import QuizForm, QuestionForm, ChoiceForm, UserRegistrationForm, QuizCreationForm

# General Views
def home(request):
    return render(request, 'home.html')

# Authentication Views
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('user_dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}! You have successfully logged in.")
                return redirect('user_dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# User Views
@login_required
def user_dashboard(request):
    subjects = Subject.objects.all()
    quizzes_completed = QuizAttempt.objects.filter(user=request.user).count()
    average_score = QuizAttempt.objects.filter(user=request.user).aggregate(Avg('score'))['score__avg'] or 0
    
    context = {
        'subjects': subjects,
        'quizzes_completed': quizzes_completed,
        'average_score': average_score,
    }
    return render(request, 'user/dashboard.html', context)

@login_required
def quiz_list(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    quizzes = Quiz.objects.filter(subject=subject)
    return render(request, 'user/quiz_list.html', {'subject': subject, 'quizzes': quizzes})

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'user/quiz_detail.html', {'quiz': quiz})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    
    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                selected_choice = Choice.objects.get(pk=selected_choice_id)
                if selected_choice.is_correct:
                    score += 1
        
        QuizResult.objects.create(user=request.user, quiz=quiz, score=score)
        return redirect('quiz_result', quiz_id=quiz.id)
    
    return render(request, 'user/take_quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    result = QuizResult.objects.filter(user=request.user, quiz=quiz).latest('completed_at')
    
    question_count = quiz.question_set.count()
    score_percentage = (result.score / question_count) * 100 if question_count > 0 else 0
    performance_level = 'excellent' if score_percentage == 100 else 'good' if score_percentage >= 70 else 'average'

    context = {
        'result': result,
        'question_count': question_count,
        'score_percentage': score_percentage,
        'performance_level': performance_level,
    }
    return render(request, 'user/quiz_result.html', context)

@login_required
def profile(request):
    results = QuizResult.objects.filter(user=request.user).order_by('-completed_at')
    return render(request, 'user/profile.html', {'results': results})

# Admin Views
@staff_member_required
def admin_dashboard(request):
    subjects = Subject.objects.all()
    quizzes = Quiz.objects.all()
    return render(request, 'admin/dashboard.html', {'subjects': subjects, 'quizzes': quizzes})

@staff_member_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizCreationForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            return redirect('admin_dashboard')
    else:
        form = QuizCreationForm()
    return render(request, 'admin/create_quiz.html', {'form': form})

@staff_member_required
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'admin/edit_quiz.html', {'form': form, 'quiz': quiz})