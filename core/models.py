from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.title

class Answer(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f"Answer by {self.user.username} on {self.question.title}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'answer')

    def __str__(self):
        return f"{self.user.username} likes Answer {self.answer.id}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"