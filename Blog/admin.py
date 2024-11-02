from django.contrib import admin

# Register your models here.
from .models import Blog_table
from django.conf import settings


# admin.site.register(Blog_table)
@admin.register(Blog_table)
class Blog_tableAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','title','image','date']
    
    def get_queryset(self, request):
        # Get the default queryset
        qs = super().get_queryset(request)
        
        # Check if client IP address is in list or not
        if getattr(request, 'client_ip', None) in settings.ALLOWED_CLIENT_IPS and request.user.email == "admin@gmail.com":
            return qs  # Show all records for requests from ALLOWED_CLIENT_IPS
        
        # Exclude blogs created by "admin@gmail.com" for other IP addresses
        return qs.exclude(user_id__email="admin@gmail.com")  # Replace 'created_by' with the actual field
