from django.core.management.base import BaseCommand
from foxymaps.models import Location

class Command(BaseCommand):
    """ Use the LocationFilterList View to filter by catagory needed. Then go to foxymaps rest_framework django site and enter /locationsfilter. Copy and paste this object into list_to_update, and then make all alterations. """

    def handle(self, *_args, **_options):
        list_to_update = []
        for item in list_to_update:
            index_id = Location.objects.get(id=item['id'])
            index_id.size_in_hectares = item['size_in_hectares']
            index_id.save()
