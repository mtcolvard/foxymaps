from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100, null=True)
    summary = models.TextField(max_length=2500, null=True)
    previous_name = models.CharField(max_length=100, null=True)
    site_location = models.CharField(max_length=100, null=True)
    postcode = models.CharField(max_length=10, null=True)
    type_of_site = models.CharField(max_length=50, null=True)
    date = models.CharField(max_length=30, null=True)
    designer = models.CharField(max_length=50, null=True)
    listed_structures = models.CharField(max_length=150, null=True)
    borough = models.CharField(max_length=50, null=True)
    site_ownership = models.CharField(max_length=50, null=True)
    site_management = models.CharField(max_length=50, null=True)
    open_to_public = models.CharField(max_length=10, null=True)
    opening_times = models.CharField(max_length=30, null=True)
    special_conditions = models.CharField(max_length=250, null=True)
    facilities = models.CharField(max_length=250, null=True)
    public_transportation = models.CharField(max_length=200, null=True)
    lon_lat = models.CharField(max_length=100, null=True)
    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)
    grid_reference = models.CharField(max_length=36, null=True)
    size_in_hectares = models.CharField(max_length=100, null=True)
    image = models.CharField(max_length=250, null=True)
    fuller_information = models.TextField(max_length=20000, null=True)
    sources_consulted = models.TextField(max_length=1000, null=True)

    def __str__(self, null=True):
        return f'{self.name}'
