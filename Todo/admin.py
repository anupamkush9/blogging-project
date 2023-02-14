from django.contrib import admin
from .models import Task
# Register your models here.
@admin.register(Task)
class Taskadmin(admin.ModelAdmin):
    list_display = ['user_id','id','title','complete','time']