from django.core.management.base import BaseCommand
from teams.models import Team, Singer
from results.models import TeamResult, SingerResult
from django.db.models import Count
from collections import OrderedDict

class Command(BaseCommand):
    help = "Make results"

    def handle(self, *args, **options):
        all_singers = Singer.objects.prefetch_related('singeroccurrence_set')
        for singer in all_singers:
            total = 0
            event_details = OrderedDict()

            occurrences = singer.singeroccurrence_set.all().order_by('event__id')
            
            for singer_occurrence in occurrences:
                points = singer_occurrence.occurrence.points
                if singer_occurrence.occurrence.outcome == 'PENALTY':
                    points = -points
                
                total += points
                event_id = singer_occurrence.event.id
                event_name = singer_occurrence.event.name

                if event_id not in event_details:
                    event_details[event_id] = {
                        "event_name": event_name,
                        "occurrences": []
                    }
                event_details[event_id]["occurrences"].append({
                    "occurrence": singer_occurrence.occurrence.occurrence,
                    "outcome": singer_occurrence.occurrence.outcome,
                    "points": points
                })

            SingerResult.objects.update_or_create(
                singer=singer,
                defaults={
                    'total_points': total,
                    'details': {"scores": event_details}
                }
            )

        all_teams = Team.objects.annotate(
            member_count=Count('teammember')
        ).filter(
            member_count__exact=5
        ).exclude(
            captain__isnull=True
        )

        for team in all_teams:
            team_total = 0
            member_details = []
            for member in team.teammember_set.all():
                singer_result = SingerResult.objects.get(singer=member.singer)
                multiplier = 2 if member.singer == team.captain else 1
                team_total += singer_result.total_points * multiplier

                member_details.append({
                    "singer": member.singer.name,
                    "total": singer_result.total_points * multiplier,
                    "is_captain": (member.singer == team.captain),
                    "scores": singer_result.details.get("scores", {})
                })
            
            TeamResult.objects.update_or_create(
                team=team,
                defaults={
                    'total_points': team_total,
                    'details': {"members": member_details}
                }
            )
        
        self.stdout.write(self.style.SUCCESS("Successfully generated results"))