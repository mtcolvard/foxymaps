from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=6000, null=False)
    href = models.CharField(max_length=6000, null=True)
    summary = models.TextField(max_length=60000, null=True)
    previous_name = models.CharField(max_length=6000, null=True)
    site_location = models.CharField(max_length=6000, null=True)
    postcode = models.CharField(max_length=6000, null=True)
    type_of_site = models.CharField(max_length=6000, null=True)
    designer = models.CharField(max_length=6000, null=True)
    listed_structures = models.CharField(max_length=6000, null=True)
    borough = models.CharField(max_length=6000, null=True)
    site_ownership = models.CharField(max_length=6000, null=True)
    site_management = models.CharField(max_length=6000, null=True)
    open_to_public = models.CharField(max_length=6000, null=True)
    opening_times = models.CharField(max_length=6000, null=True)
    special_conditions = models.CharField(max_length=10000, null=True)
    facilities = models.CharField(max_length=10000, null=True)
    lon_lat = models.CharField(max_length=6000, unique=True, null=False)
    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)
    grid_reference = models.CharField(max_length=6000, null=True)
    on_eh_national_register = models.CharField(max_length=6000, null=True)
    eh_grade = models.CharField(max_length=6000, null=True)
    on_local_list = models.CharField(max_length=6000, null=True)
    in_conservation_area = models.CharField(max_length=6000, null=True)
    tree_preservation_order = models.CharField(max_length=6000, null=True)
    nature_conservation_area = models.CharField(max_length=6000, null=True)
    green_belt = models.CharField(max_length=6000, null=True)
    metropolitan_open_land = models.CharField(max_length=6000, null=True)
    special_policy_area = models.CharField(max_length=6000, null=True)
    other_la_designation = models.CharField(max_length=6000, null=True)
    image = models.CharField(max_length=10000, null=True)
    size_in_hectares = models.FloatField(null=True)
    size_in_hectares_raw = models.CharField(max_length=1000, null=True)
    size_in_hectares_regex = models.CharField(max_length=1000, null=True)
    size_in_hectares_error = models.BooleanField()

    def __str__(self, null=True):
        return f'{self.name}'
