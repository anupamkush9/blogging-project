from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField

class Blog_table(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)    #user_id is the username
    title=models.CharField(max_length=150)
    Description=FroalaField()
    date=models.DateTimeField(auto_now_add=True,null=True)
    image=models.ImageField(upload_to='Blog/images',default='')
