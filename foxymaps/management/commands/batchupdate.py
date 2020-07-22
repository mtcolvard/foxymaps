from django.core.management.base import BaseCommand
from foxymaps.models import Location

class Command(BaseCommand):

    def handle(self, *_args, **_options):

        list_to_update = Location.objects.filter(size_in_hectares_error=True)

        for item in list_to_update:
            index_id = Location.objects.get(id=item['id'])
            index_id.size_in_hectares = item['size_in_hectares']
            index_id.save()
