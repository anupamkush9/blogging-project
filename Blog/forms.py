from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from .models import Blog_table
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginForm(AuthenticationForm):
 username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control'}))
 password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}))

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'email': 'Email'}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),  # Correct widget usage
        }
  
    def save(self, commit=True):
      user = super(SignUpForm, self).save(commit=False)
      user.username = self.cleaned_data['email']  # Set username as email
      user.email = self.cleaned_data['email']
      if commit:
          user.save()
      return user

class BlogForm(forms.ModelForm):
 class Meta:
  model = Blog_table
  fields = ['Description']

#
# class Editing_blog(forms.ModelForm):
#  class Meta:
#   model = Blog_table
#   fields = ['title', 'Description']

