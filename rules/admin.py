from django.contrib import admin
from .models import Rules, Occurrence

class OccurrenceAdmin(admin.ModelAdmin):
    fields = ("occurence", "outcome", "points")

admin.site.register(Rules)
admin.site.register(Occurrence, OccurrenceAdmin)

