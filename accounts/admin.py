from django.contrib import admin
from accounts.models import blogingUser
from django.contrib.auth.admin import UserAdmin

class blogingUserAdmin(UserAdmin):
    list_display = ['email']

# Register your models here.
admin.site.register(blogingUser, blogingUserAdmin)