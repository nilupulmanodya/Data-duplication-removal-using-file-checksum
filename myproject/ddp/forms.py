from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import temUploads, Shared
from django import forms


class createUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class temUpload(ModelForm):
    class Meta:
        model = temUploads
        fields = ['title', 'tem_file']

class fileShare(ModelForm):
    class Meta:
        model = Shared
        fields = '__all__'
        exclude = ['shared_by','s_hash','s_title']
