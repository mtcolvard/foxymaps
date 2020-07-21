import re
import urllib.request
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from foxymaps.models import Location

class Command(BaseCommand):

    def scrape_location(self, url):
        x = urllib.request.urlopen(f'https://londongardenstrust.org/conservation/inventory/{url}')
        href = url
        soup = BeautifulSoup(x, 'html.parser')

        citymapper_href = soup.find(href=re.compile("citymapper")).get('href')
        citymapper_href_edit1 = citymapper_href.replace('https://citymapper.com/directions?endcoord=', '').split('&', 1)[0].split(',')
        citymapper_href_edit2 = [float(i) for i in citymapper_href_edit1]
        citymapper_href_edit2.reverse()
        citymapper_lon = citymapper_href_edit2[0]
        citymapper_lat = citymapper_href_edit2[1]
        citymapper_lon_lat = f'{citymapper_lon},{citymapper_lat}'

        if soup.find(id='photos') == None:
            image_formatted = 'https://londongardenstrust.org/inventory/images/sitepics/THM033-site.jpg'
        else:
            image = ([str(soup.find(id='photos').img)].pop().split('src="', 1)[1]).replace('" style="image-orientation: none;display:inline"/>', '')
            image_formatted = ''.join(['https://londongardenstrust.org/', image])

        previous_name_raw = soup.find("dt", string="Previous / Other name:")
        if previous_name_raw is None:
            previous_name = None
        else:
            previous_name = previous_name_raw.find_next("dd").string

        size_in_hectares_raw = soup.find("dt", string="Size in hectares:").find_next("dd").string
        size_in_hectares_regex = None
        size_in_hectares_error = False
        if size_in_hectares_raw is None:
            size_in_hectares = None
        else:
            size_in_hectares_formatted_one = re.sub(r'(c\.|c)', '', size_in_hectares_raw)
            size_in_hectares_formatted_two = re.sub(r'[^\d.]+', '', size_in_hectares_formatted_one)
            size_in_hectares_regex = str(size_in_hectares_formatted_two)
            try:
                size_in_hectares = float((size_in_hectares_formatted_two).split()[0])
            except (TypeError, ValueError, IndexError):
                size_in_hectares = 0.0
                size_in_hectares_error = True

        name = soup.find('title').find_next('title').string
        summary = soup.find(id='summary').p.string
        site_location = soup.find("dt", string="Site location:").find_next("dd").string
        postcode = soup.find("dt", string="Postcode:").find_next("dd").string
        type_of_site = soup.find("dt", string="Type of site: ").find_next("dd").string
        designer = soup.find("dt", string="Designer(s):").find_next("dd").string
        listed_structures = soup.find("dt", string="Listed structures:").find_next("dd").string
        borough = soup.find("dt", string="Borough:").find_next("dd").string
        site_ownership = soup.find("dt", string="Site ownership:").find_next("dd").string
        site_management = soup.find("dt", string="Site management:").find_next("dd").string
        open_to_public = soup.find("dt", string="Open to public? ").find_next("dd").string
        opening_times = str(soup.find("dt", string="Opening times:").find_next("dd")).split('<b')[0].lstrip('<dd>').lstrip().split('</dd>')[0]
        special_conditions = soup.find("dt", string="Special conditions:").find_next("dd").string
        facilities = soup.find("dt", string="Facilities:").find_next("dd").string
        grid_reference = soup.find("dt", string="Grid ref: ").find_next("dd").string
        on_eh_national_register = soup.find("dt", string="On EH National Register :").find_next("dd").string
        eh_grade = soup.find("dt", string="EH grade:").find_next("dd").string
        on_local_list = soup.find("dt", string="On Local List:").find_next("dd").string
        in_conservation_area = soup.find("dt", string="In Conservation Area: ").find_next("dd").string
        tree_preservation_order = soup.find("dt", string="Tree Preservation Order: ").find_next("dd").string
        green_belt = soup.find("dt", string="Green Belt: ").find_next("dd").string
        metropolitan_open_land = soup.find("dt", string="Metropolitan Open Land: ").find_next("dd").string
        special_policy_area = soup.find("dt", string="Special Policy Area: ").find_next("dd").string
        other_la_designation = soup.find("dt", string="Other LA designation: ").find_next("dd").string

        nature_conservation_area_pre = soup.find("dt", string="Nature Conservation Area: ").find_next("dd").string
        if nature_conservation_area_pre is None:
            nature_conservation_area = None
        else:
            nature_conservation_area = nature_conservation_area_pre.split()[0]

        data = {
            'name': name,
            'href': href,
            'summary': summary,
            'previous_name': previous_name,
            'site_location': site_location,
            'postcode': postcode,
            'type_of_site': type_of_site,
            'designer': designer,
            'listed_structures': listed_structures,
            'borough': borough,
            'site_ownership': site_ownership,
            'site_management': site_management,
            'open_to_public': open_to_public,
            'opening_times': opening_times,
            'special_conditions': special_conditions,
            'facilities': facilities,
            'lon_lat': citymapper_lon_lat,
            'lon': citymapper_lon,
            'lat': citymapper_lat,
            'grid_reference': grid_reference,
            'size_in_hectares': size_in_hectares,
            'size_in_hectares_raw': size_in_hectares_raw,
            'size_in_hectares_regex': size_in_hectares_regex,
            'size_in_hectares_error': size_in_hectares_error,
            'on_eh_national_register': on_eh_national_register,
            'eh_grade': eh_grade,
            'on_local_list': on_local_list,
            'in_conservation_area': in_conservation_area,
            'tree_preservation_order': tree_preservation_order,
            'nature_conservation_area': nature_conservation_area,
            'green_belt': green_belt,
            'metropolitan_open_land': metropolitan_open_land,
            'special_policy_area': special_policy_area,
            'other_la_designation': other_la_designation,
            'image': image_formatted,
        }

        data_formatted = {k:(v.rstrip() if isinstance(v, str) else v) for (k, v) in data.items()}
        print(size_in_hectares_error)
        print(size_in_hectares_raw)
        print(size_in_hectares_regex)
        location = Location(**data_formatted)
        location.save()


    def handle(self, *_args, **_options):
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Barking+%26+Dagenham&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Barnet&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Bexley&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Brent&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Bromley&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Camden&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=City+of+London&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Croydon&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Ealing&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Enfield&type=%25&keyword=&Submit=Search')
#checked
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Greenwich&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Hackney&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Hammersmith+%26+Fulham&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Haringey&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Harrow&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Havering&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Hillingdon&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Hounslow&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Islington&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Kensington+%26+Chelsea&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Kingston&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Lambeth&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Lewisham&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Merton&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Newham&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Redbridge&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Richmond&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Southwark&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Sutton&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Tower+Hamlets&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Waltham+Forest&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Wandsworth&type=%25&keyword=&Submit=Search')
        # x = urllib.request.urlopen('https://londongardenstrust.org/conservation/inventory/sitelist/?sitename=&borough=Westminster&type=%25&keyword=&Submit=Search')
        # #
        # soup = BeautifulSoup(x, 'html.parser')
        # links = soup.find(class_="lgt-nav").find_all('a')
        # for link in links:
        #     href = link.get('href')
        #     print(href)
        #     self.scrape_location(href)
        #
        links =  [ 'site-record?ID=WST145&sitename=Westminster+Abbey+Precincts+-+The+College+Garden', 'site-record?ID=WST142&sitename=Westminster+Abbey+Precincts+%2F+Westminster+School+-+Dean%27s+Yard', 'site-record?ID=WST146&sitename=Westminster+Cathedral+Piazza', 'site-record?ID=WST147&sitename=Wilton+Crescent+Garden+%2A', 'site-record?ID=WST148&sitename=Wool+House+Garden', 'site-record?ID=WST149&sitename=York+Terrace+West'


]
        for href in links:
            print(href)
            self.scrape_location(href)




        # b = Location.objects.get(id=2489)
        # b.delete()
