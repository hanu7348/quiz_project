# quiz_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Subject, Quiz, Question, Choice

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['subject', 'title', 'description', 'time_limit']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']

class QuizCreationForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
    time_limit = forms.IntegerField(help_text="Time limit in minutes")
    
    question_1 = forms.CharField(widget=forms.Textarea)
    question_1_choice_1 = forms.CharField(max_length=200)
    question_1_choice_2 = forms.CharField(max_length=200)
    question_1_choice_3 = forms.CharField(max_length=200)
    question_1_choice_4 = forms.CharField(max_length=200)
    question_1_correct = forms.ChoiceField(choices=[(1, 'Choice 1'), (2, 'Choice 2'), (3, 'Choice 3'), (4, 'Choice 4')])

    # You can add more questions and choices as needed
    # For simplicity, I've only included one question, but you can extend this

    def save(self):
        quiz = Quiz.objects.create(
            subject=self.cleaned_data['subject'],
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            time_limit=self.cleaned_data['time_limit']
        )

        question = Question.objects.create(
            quiz=quiz,
            text=self.cleaned_data['question_1']
        )

        for i in range(1, 5):
            Choice.objects.create(
                question=question,
                text=self.cleaned_data[f'question_1_choice_{i}'],
                is_correct=(str(i) == self.cleaned_data['question_1_correct'])
            )

        return quiz
    
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user