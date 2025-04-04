from django.core.management.base import BaseCommand, CommandError
from rules.models import Event, Occurrence, SingerOccurrence
from teams.models import Singer

class Command(BaseCommand):
    help = "Score team members for a thing that happened during a given event"

    def add_arguments(self, parser):
        parser.add_argument("occurrence", type=int)
        parser.add_argument("event", type=int)
        parser.add_argument("singers", nargs="+", type=int)

    def handle(self, *args, **options):

        try:
            event = Event.objects.get(pk=options["event"])
            occurrence = Occurrence.objects.get(pk=options["occurrence"])
        except Exception as e:
            raise CommandError(f'Exception: {e}')

        for singer_id in options["singers"]:
            try:
                singer = Singer.objects.get(pk=singer_id)
            except Singer.DoesNotExist:
                raise CommandError(f'Singer {singer_id} does not exist')
            
            singer_occurrences = []
            singer_occurrences.append(
                SingerOccurrence(singer=singer, occurrence=occurrence, event=event)
            )

            try:
                so = SingerOccurrence.objects.bulk_create(singer_occurrences)
            except Exception as e:
                raise CommandError(f'Exception {e} while creating singer occurrences')

        self.stdout.write(self.style.SUCCESS("Successfully assigned scores"))