from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
User=get_user_model()

class UserCreationForm(AdminUserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "image")

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username", "email", "image")

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
