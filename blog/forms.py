from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'slug']

    def save(self, user, commit=True):
        instance = super().save(commit=False)
        instance.user = user
        if commit:
            instance.save()
        return instance

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class EditProfileForm(UserChangeForm):
    password_change = PasswordChangeForm(User)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def is_valid(self):
        return super().is_valid() and self.password_change.is_valid()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.password_change.save()
       
