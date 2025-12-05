from django.core.management.base import BaseCommand
from Warehouse_System.models import Localization

class Command(BaseCommand):

    def handle(self, *args, **options):
        names = ['P','O','H']
        for name in names:
            for number in range(10,13+1):
                for row in range(0,9+1):
                    for height in range(1,4+1):
                        if number == 10 and row == 0:
                            continue
                        else:
                            lokalization = (f'{name}{number}{row}0{height}')
                            Localization.objects.get_or_create(localization_name=lokalization)
