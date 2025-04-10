from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserChangeForm
from django.contrib.auth import get_user_model
User=get_user_model()
import logging
logger = logging.getLogger('custom_logger')
from django.contrib.auth.decorators import login_required
from common import UtilityFunctions
from django.shortcuts import render, get_object_or_404

class RegisterView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login') 
    template_name = 'registration/register.html'

@login_required
def ProfileView(request):
    user = request.user
    return render(request, "users/profile.html", {
        "user": user
    })

@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    success_message = "User profile information successfully updated"

    if request.method == "POST":
        form = UserChangeForm(request.POST, request.FILES, instance=user)

        if form.is_valid():

            try:
                user = form.save(commit=False)
                user.save()
            except Exception as e:
                logger.error(f"Exception while editing user profile: {e}")
                return UtilityFunctions.toastTrigger(request, 204, f"Failed to edit user profile", "error")
            
            return UtilityFunctions.toastTrigger(request, 204, success_message, "success", [{"userProfileChanged": None}])
        else:
        
            return render(request, "users/edit-profile.html", {
                "user": user,
                "form": form,
            })

    else:
        form = UserChangeForm(instance=user)
    
    return render(request, "users/edit-profile.html", {
        "user": user,
        "form": form,
    })

@login_required
def reload_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    return render(request, "users/profile-reload.html", {
        "user": user
    })