from django.contrib import admin
from .models import Rules, Occurrence, Event

class OccurrenceAdmin(admin.ModelAdmin):
    fields = ("occurrence", "outcome", "points")

admin.site.register(Rules)
admin.site.register(Occurrence, OccurrenceAdmin)
admin.site.register(Event)

