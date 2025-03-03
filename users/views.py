from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Team, Member
from django.urls import reverse
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = "teams/index.html"
    context_object_name = "teams_by_user_list"

    def get_queryset(self):
        #return Team.objects.filter(data_pub__lte=timezone.now(),scelta__isnull=False).distinct().order_by("-data_pub")[:5]
        return "ecco"
    
class ViewTeam(generic.DetailView):
    model = Team
    template_name = "teams/view-team.html"

    def get_queryset(self):
        #return Team.objects.filter(data_pub__lte=timezone.now(), scelta__isnull=False).distinct()
        return "ecco"

""""
def vota(richiesta, domanda_id):
    domanda = get_object_or_404(Team, pk=domanda_id)

    try:
        fatta_scelta = domanda.scelta_set.get(pk=richiesta.POST['scelta'])
    except (KeyError, Scelta.DoesNotExist):
        return render(richiesta, "teams/view-team.html", {
            "domanda": domanda,
            "messagio_error": "Non hai selezionato una scelta"
        })
    else:
        fatta_scelta.voti = F("voti") + 1
        fatta_scelta.save()
        return HttpResponseRedirect(reverse("polls:risultati", args=(domanda.id,)))
"""
