from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model
User=get_user_model()
max_usable_points = settings.MAXIMUM_USABLE_POINTS
from django.conf.urls.static import static

class Singer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    song = models.CharField(max_length=100)
    singer_image = models.ImageField(null=True)
    points_cost = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(max_usable_points)], default=0)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    team_image = models.ImageField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    captain = models.ForeignKey(Singer, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def reached_member_limit(self):
        member_limit = settings.MEMBERS_PER_TEAM
        members_in_team_count = self.teammember_set.all().count()
        return members_in_team_count >= member_limit
    
    def reached_points_limit(self):
        points_limit = settings.MAXIMUM_USABLE_POINTS
        points_used = 0
        members_in_team = self.teammember_set.all()
        for member in members_in_team:
            singer = Singer.objects.get(pk=member.singer_id)
            points_used += singer.points_cost
        return points_used >= points_limit
    
    def get_members_with_singers(self):
        return [team_member.singer for team_member in self.teammember_set.select_related('singer').all()]

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('team', 'singer')

    def __str__(self):
        return str(self.team_id) + ';' + str(self.singer)
    
    def team_contains_member(self, team_id, singer_id):
        member_in_team = self.objects.filter(team=team_id, singer=singer_id)
        return member_in_team.count() > 0
    
    def is_captain(self, team_id, singer_id):
        team = Team.objects.get(pk=team_id)
        captain_id = team.captain_id
        if captain_id == singer_id:
            return True
            
        return False
    