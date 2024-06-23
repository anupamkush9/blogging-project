from django.contrib import admin
from .models import Blog_table

from django.contrib.auth.models import Permission
from django.db import transaction
from .models import UserPermissionCredit

class UserPermissionCreditAdmin(admin.ModelAdmin):
    fields = ['user', 'permission', 'credits']
    list_display = ['user', 'permission', 'credits']

    def save_model(self, request, obj, form, change):
        try:
            with transaction.atomic():
                # First, save the UserPermissionCredit object
                super().save_model(request, obj, form, change)
                
                # Retrieve permission and user details
                permission_name = obj.permission
                user = obj.user

                # Assign the add and view permissions to the user
                for each_permission in ["add", "view"]:
                    model_permission_code_name = f"{each_permission}_{permission_name}"
                    model_permission = Permission.objects.get(codename__iexact=model_permission_code_name)
                    user.user_permissions.add(model_permission)
                    # Ref : https://testdriven.io/blog/django-permissions/ 
                    # Ref : https://testdriven.io/blog/django-permissions/ 
        except Permission.DoesNotExist:
            print(f"Permission {model_permission_code_name} does not exist.")
        except Exception as e:
            print("Exception is", e)
            import traceback
            print(traceback.format_exc())

    def delete_model(self, request, obj):
        try:
            with transaction.atomic():
                user = obj.user
                permission_name = obj.permission
                # Remove the permissions associated with the UserPermissionCredit instance
                for each_permission in ["add", "view"]:
                    model_permission_code_name = f"{each_permission}_{permission_name}"
                    model_permission = Permission.objects.get(codename__iexact=model_permission_code_name)
                    user.user_permissions.remove(model_permission)
                    # Ref : https://testdriven.io/blog/django-permissions/ 
                    # Ref : https://testdriven.io/blog/django-permissions/ 
                    
                # Now delete the UserPermissionCredit object
                obj.delete()
        except Permission.DoesNotExist:
            print(f"Permission {model_permission_code_name} does not exist.")
        except Exception as e:
            print("Exception is", e)
            import traceback
            print(traceback.format_exc())

# admin.site.register(Blog_table)
@admin.register(Blog_table)
class Blog_tableAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','title','image','date']

# Register the admin class
admin.site.register(UserPermissionCredit, UserPermissionCreditAdmin)