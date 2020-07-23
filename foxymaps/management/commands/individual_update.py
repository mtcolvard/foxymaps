from django.core.management.base import BaseCommand
from foxymaps.models import Location

class Command(BaseCommand):

    def handle(self, *_args, **_options):
        # correct_number = 10
        # error_number = 211
        # location_to_update = Location.objects.filter(size_in_hectares=error_number)
        # location_id = location_to_update[0].id
        # location_object = Location.objects.get(id=location_id)
        # print(location_to_update)
        # print(location_object)
        # location_object.size_in_hectares = correct_number
        # location_object.save()
        # location_object = Location.objects.get(id=location_id)
        # print(location_object.size_in_hectares)
        # print(error_number)


        location_ids = Location.objects.filter(open_to_public='Partially')
        for item in location_ids:
            location_id = item.id
            yes = 'Yes'
            location_object = Location.objects.get(id=location_id)
            print(location_object)
            location_object.open_to_public = yes
            location_object.save()
            location_object = Location.objects.get(id=location_id)
            print(location_object.open_to_public)
