from django.core.management.base import BaseCommand, CommandError
from adopts.actions import create_adopt
from adopts.models import Adopt


class Command(BaseCommand):
    help = 'Adds an adopt'

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='+', type=str)
        parser.add_argument('short_name', nargs='+', type=str)

    def handle(self, *args, **options):
        name = options["name"][0]
        short_name = options["short_name"][0]

        has_adopt = Adopt.objects.filter(short_name=short_name).exists()
        if has_adopt:
            raise CommandError(
                f"Adopt with short name {short_name} already exists")

        adopt = create_adopt(name=name, short_name=short_name, width=0, height=0,
                             gen_caption="Thank you for your purchase! Here is your drop off: \n\n[img]")

        print(
            f"Adopt {adopt.id} created; please use the superadmin panel to add mods")
