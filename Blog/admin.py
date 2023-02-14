from django.contrib import admin

# Register your models here.
from .models import Blog_table


# admin.site.register(Blog_table)
@admin.register(Blog_table)
class Blog_tableAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','title','image','date']