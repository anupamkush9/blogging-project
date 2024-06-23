from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from django.db import models

class Blog_table(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)    #user_id is the username
    title=models.CharField(max_length=150)
    Description=FroalaField()
    date=models.DateTimeField(auto_now_add=True,null=True)
    image=models.ImageField(upload_to='Blog/images',default='')

def getpermissionchoices():
    features_permissions_list = []
    features_permissions_list.append(( "blog_table", "Blog Table"))
    return features_permissions_list

class UserPermissionCredit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.CharField(max_length=255, choices=getpermissionchoices(), blank=True, null=True)
    credits = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.permission} - {self.credits} credits"
