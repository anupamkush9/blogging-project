from django.contrib import admin
from accounts.models import blogingUser

class blogingUserAdmin(admin.ModelAdmin):
    list_display = ['email']

# Register your models here.
admin.site.register(blogingUser, blogingUserAdmin)