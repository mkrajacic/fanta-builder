from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm

from .models import User

class UserCreationForm(AdminUserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "image", "teams_count")

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username", "email", "image", "teams_count")