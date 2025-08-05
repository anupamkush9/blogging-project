from django.contrib import admin
from .models import Task
# Register your models here.
@admin.register(Task)
class Taskadmin(admin.ModelAdmin):
    list_display = ['user_id','id','title','complete','time']
    actions = ['mark_as_complete', 'mark_as_incomplete']

    @admin.action(description="Mark selected tasks as complete")
    def mark_as_complete(self, request, queryset):
        updated = queryset.update(complete=True)
        self.message_user(request, f"{updated} task(s) marked as complete.")

    @admin.action(description="Mark selected tasks as incomplete")
    def mark_as_incomplete(self, request, queryset):
        updated = queryset.update(complete=False)
        self.message_user(request, f"{updated} task(s) marked as incomplete.")
