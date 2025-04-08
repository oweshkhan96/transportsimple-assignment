from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, QuestionForm, AnswerForm
from .models import Question, Answer, Like
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Notification

def home(request):
    questions = Question.objects.all().order_by('-timestamp')
    return render(request, 'core/home.html', {'questions': questions})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            messages.success(request, "Question posted successfully!")
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'core/post_question.html', {'form': form})

def view_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all().order_by('-timestamp')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to post an answer.")
            return redirect('login')
        
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()

            if request.user != question.user:
                Notification.objects.create(
                    user=question.user,
                    message=f"{request.user.username} answered your question: '{question.title}'"
                )

            messages.success(request, "Answer posted successfully!")
            return redirect('view_question', question_id=question.id)
    else:
        form = AnswerForm()

    context = {
        'question': question,
        'answers': answers,
        'form': form
    }
    return render(request, 'core/question.html', context)

@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    like, created = Like.objects.get_or_create(user=request.user, answer=answer)

    if created:
        messages.success(request, "You liked the answer!")

        if request.user != answer.user:
            Notification.objects.create(
                user=answer.user,
                message=f"{request.user.username} liked your answer."
            )
    else:
        messages.info(request, "You have already liked this answer.")

    return redirect('view_question', question_id=answer.question.id)

@login_required
def notifications(request):
    notifs = request.user.notifications.order_by('-timestamp')
    return render(request, 'core/notifications.html', {'notifications': notifs})


def custom_logout(request):
    logout(request)
    return redirect('home')