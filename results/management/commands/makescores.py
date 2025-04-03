from django.core.management.base import BaseCommand, CommandError
from rules.models import Event, Occurrence, MemberOccurrence
from teams.models import Singer, TeamMember

class Command(BaseCommand):
    help = "Score team members for a thing that happened during a given event"

    def add_arguments(self, parser):
        parser.add_argument("occurrence", type=int)
        parser.add_argument("event", type=int)
        parser.add_argument("singers", nargs="+", type=int)

    def handle(self, *args, **options):

        try:
            event = Event.objects.get(pk=options["event"])
        except Event.DoesNotExist:
            raise CommandError(f'Event {options["event"]} does not exist')
        
        try:
            occurrence = Occurrence.objects.get(pk=options["occurrence"])
        except Occurrence.DoesNotExist:
            raise CommandError(f'Occurrence {options["occurrence"]} does not exist')

        for singer_id in options["singers"]:
            try:
                singer = Singer.objects.get(pk=singer_id)
            except Singer.DoesNotExist:
                raise CommandError(f'Singer {singer_id} does not exist')
            
            # fetch only team members from teams with valid nr of members and captain selected?
            members_to_score = TeamMember.objects.filter(singer=singer_id)
            member_occurrences = []
            for member in members_to_score:
                member_occurrences.append(
                    MemberOccurrence(occurrence_id=occurrence.id, team_member_id=member.id, event_id=event.id)
                )

            try:
                mh = MemberOccurrence.objects.bulk_create(member_occurrences)
            except Exception as e:
                raise CommandError(f'Exception {e} while creating member occurrences')

        self.stdout.write(self.style.SUCCESS("Successfully assigned scores"))