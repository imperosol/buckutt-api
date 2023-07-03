from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Supprime la db et la repeuple avec les données de test"

    def handle(self, *args, **options):
        call_command("flush", "--noinput")
        ContentType.objects.all().delete()
        call_command("loaddata", "fixtures.json")
