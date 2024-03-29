# Generated by Django 3.0.8 on 2020-07-20 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('href', models.CharField(max_length=100, null=True)),
                ('summary', models.TextField(max_length=2500, null=True)),
                ('previous_name', models.CharField(max_length=100, null=True)),
                ('site_location', models.CharField(max_length=100, null=True)),
                ('postcode', models.CharField(max_length=10, null=True)),
                ('type_of_site', models.CharField(max_length=50, null=True)),
                ('designer', models.CharField(max_length=50, null=True)),
                ('listed_structures', models.CharField(max_length=150, null=True)),
                ('borough', models.CharField(max_length=50, null=True)),
                ('site_ownership', models.CharField(max_length=50, null=True)),
                ('site_management', models.CharField(max_length=50, null=True)),
                ('open_to_public', models.CharField(max_length=10, null=True)),
                ('opening_times', models.CharField(max_length=30, null=True)),
                ('special_conditions', models.CharField(max_length=250, null=True)),
                ('facilities', models.CharField(max_length=250, null=True)),
                ('lon_lat', models.CharField(max_length=100, unique=True)),
                ('lon', models.FloatField(null=True)),
                ('lat', models.FloatField(null=True)),
                ('grid_reference', models.CharField(max_length=36, null=True)),
                ('on_eh_national_register', models.CharField(max_length=50, null=True)),
                ('eh_grade', models.CharField(max_length=50, null=True)),
                ('on_local_list', models.CharField(max_length=50, null=True)),
                ('in_conservation_area', models.CharField(max_length=50, null=True)),
                ('tree_preservation_order', models.CharField(max_length=50, null=True)),
                ('nature_conservation_area', models.CharField(max_length=50, null=True)),
                ('green_belt', models.CharField(max_length=50, null=True)),
                ('metropolitan_open_land', models.CharField(max_length=50, null=True)),
                ('special_policy_area', models.CharField(max_length=50, null=True)),
                ('other_la_designation', models.CharField(max_length=50, null=True)),
                ('image', models.CharField(max_length=250, null=True)),
                ('size_in_hectares', models.FloatField(null=True)),
                ('size_in_hectares_raw', models.CharField(max_length=60, null=True)),
                ('size_in_hectares_regex', models.CharField(max_length=60, null=True)),
                ('size_in_hectares_error', models.BooleanField()),
            ],
        ),
    ]
