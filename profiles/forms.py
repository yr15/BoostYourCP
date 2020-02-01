from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import  Profile,Post
class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username','email','password1','password2']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['collegeName', 'city','codechefId','codeforceId','hackerrankId','MailChoice']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = [ 'username' , 'email']

class CreatePostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = [ 'title' , 'post_data']