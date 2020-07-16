from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField(max_length=2500)
    previous_name = models.CharField(max_length=100)
    site_location = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    type_of_site = models.CharField(max_length=50)
    date = models.CharField(max_length=30)
    designer = models.CharField(max_length=50)
    listed_structures = models.CharField(max_length=150)
    borough = models.CharField(max_length=50)
    site_ownership = models.CharField(max_length=50)
    site_management = models.CharField(max_length=50)
    open_to_public = models.CharField(max_length=10)
    opening_times = models.CharField(max_length=30)
    special_conditions = models.CharField(max_length=250)
    facilities = models.CharField(max_length=250)
    public_transportation = models.CharField(max_length=200)
    lon_lat = models.CharField(max_length=100)
    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)
    grid_reference = models.CharField(max_length=36)
    size_in_hectares = models.CharField(max_length=100)
    image = models.CharField(max_length=250)
    fuller_information = models.TextField(max_length=20000)
    sources_consulted = models.TextField(max_length=1000)

    def __str__(self):
        return f'{self.name}'
