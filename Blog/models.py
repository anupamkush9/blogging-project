from django.db import models
from froala_editor.fields import FroalaField
from django.contrib.auth import get_user_model
User = get_user_model()

class Blog_table(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)    #user_id is the username
    title=models.CharField(max_length=150)
    # here Description d should be in small characters as per model field naming convention
    Description=FroalaField()
    image=models.ImageField(upload_to='Blog/images', default='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Set once when the record is created
    updated_at = models.DateTimeField(auto_now=True)      # Updated automatically on every save

    def __str__(self):
        return self.title
