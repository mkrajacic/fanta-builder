from django import forms
from django.forms import ModelForm
from teams.models import Team
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger('custom_logger')

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ["name", "team_image"]

    def clean_name(self):
        data = self.cleaned_data["name"]
        
        return data
    
    def clean_team_image(self):
        data = self.cleaned_data.get("team_image")
        
        if data and hasattr(data, 'file'):
            return data  # Return uploaded file
        
        if self.instance and self.instance.team_image:
            return self.instance.team_image
        
        return '/unknown.svg'
