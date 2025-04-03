from django.core.management.base import BaseCommand
from teams.models import Team, Singer
from rules.models import Event
from results.models import TeamResult
import json

class Command(BaseCommand):
    help = "Make results"

    def handle(self, *args, **options):
        # fetch only teams with valid nr of members and captain selected?
        all_teams = Team.objects.all()
        all_events = Event.objects.all()

        for team in all_teams:
            total_points = 0
            team_results = {
                "events": []
            }

            for event in all_events:
                event_entry = {
                    "event": event.name,
                    "member_results": []
                }

                for member in team.teammember_set.all():
                    singer = Singer.objects.get(pk=member.singer_id)
                    member_data = {
                        "singer": singer.name,
                        "points_assigned_for": [],
                        "total_for_member": 0
                    }

                    mo_entries = member.memberoccurrence_set.filter(event=event)
                    for entry in mo_entries:
                        occurrence = entry.occurrence
                        entry_data = {
                            "title": occurrence.occurence,
                            "points": occurrence.points,
                            "type": occurrence.outcome
                        }
                        
                        if occurrence.outcome == 'BONUS':
                            member_data["total_for_member"] += occurrence.points
                            total_points += occurrence.points
                        else:
                            member_data["total_for_member"] -= occurrence.points
                            total_points -= occurrence.points
                            
                        member_data["points_assigned_for"].append(entry_data)

                    event_entry["member_results"].append(member_data)

                team_results["events"].append(event_entry)
            
            self.stdout.write(
                self.style.SUCCESS(json.dumps(team_results, indent=2))
            )

            try:
                if TeamResult.objects.filter(team=team).exists():
                    team_result = TeamResult.objects.get(team=team)
                    team_result.total_points = total_points
                    team_result.details = team_results
                    team_result.save()
                else:
                    TeamResult.objects.create(team=team, total_points=total_points, details=team_results)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error while adding team result: {e}")
                )
