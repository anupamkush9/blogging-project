from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Task(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=70)
    time=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)