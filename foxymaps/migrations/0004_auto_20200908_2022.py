# Generated by Django 3.1.1 on 2020-09-08 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foxymaps', '0003_auto_20200908_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='borough',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='designer',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='eh_grade',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='facilities',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='green_belt',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='grid_reference',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='href',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='image',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='in_conservation_area',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='listed_structures',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='lon_lat',
            field=models.CharField(max_length=300, unique=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='metropolitan_open_land',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='location',
            name='nature_conservation_area',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='on_eh_national_register',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='on_local_list',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='open_to_public',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='opening_times',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='other_la_designation',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='postcode',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='previous_name',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='site_location',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='site_management',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='site_ownership',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='special_conditions',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='special_policy_area',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='summary',
            field=models.TextField(max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='tree_preservation_order',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='type_of_site',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
