from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # User authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),


    # Question routes
    path('post-question/', views.post_question, name='post_question'),
    path('question/<int:question_id>/', views.view_question, name='view_question'),

    # Answer like route
    path('like/<int:answer_id>/', views.like_answer, name='like_answer'),

    # Notifications
    path('notifications/', views.notifications, name='notifications'),

]
