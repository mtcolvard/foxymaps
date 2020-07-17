import re
import urllib.request
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from foxymaps.models import Location

class Command(BaseCommand):

    def scrape_location(self, url):
        x = urllib.request.urlopen(f'https://londongardenstrust.org/conservation/inventory/site-record/?{url}')

        # x = urllib.request.urlopen(f'https://londongardenstrust.org/conservation/inventory/site-record/?ID=BAD001')

        # x = urllib.request.urlopen('http://www.londongardensonline.org.uk/search-advanced-results.php?borough=%25&type=%25&keyword=&Submit=Search')
        # print(x.read())
        soup = BeautifulSoup(x, 'html.parser')
        # print(soup.prettify())

        citymapper_href = soup.find(href=re.compile("citymapper")).get('href')
        citymapper_href_edit1 = citymapper_href.replace('https://citymapper.com/directions?endcoord=', '').split('&', 1)[0].split(',')
        citymapper_href_edit2 = [float(i) for i in citymapper_href_edit1]
        citymapper_href_edit2.reverse()
        citymapper_lon = citymapper_href_edit2[0]
        citymapper_lat = citymapper_href_edit2[1]
        citymapper_lon_lat = f'{citymapper_lon},{citymapper_lat}'
        #
        if soup.find(id='photos') == None:
            image_formatted = 'https://londongardenstrust.org/inventory/images/sitepics/THM033-site.jpg'
        else:
            image = ([str(soup.find(id='photos').img)].pop().split('src="', 1)[1]).replace('" style="image-orientation: none;display:inline"/>', '')
            image_formatted = ''.join(['https://londongardenstrust.org/', image])

        if soup.find("dt", string="Previous / Other name:") == None:
            previous_name = None
        else:
            previous_name = soup.find("dt", string="Previous / Other name:").find_next("dd").string

        name = soup.find('title').find_next('title').string
        summary = soup.find(id='summary').p.string
        site_location = soup.find("dt", string="Site location:").find_next("dd").string
        postcode = soup.find("dt", string="Postcode:").find_next("dd").string
        type_of_site = soup.find("dt", string="Type of site: ").find_next("dd").string
        date = soup.find("dt", string="Date(s):").find_next("dd").string
        designer = soup.find("dt", string="Designer(s):").find_next("dd").string
        listed_structures = soup.find("dt", string="Listed structures:").find_next("dd").string
        borough = soup.find("dt", string="Borough:").find_next("dd").string
        site_ownership = soup.find("dt", string="Site ownership:").find_next("dd").string
        site_management = soup.find("dt", string="Site management:").find_next("dd").string
        open_to_public = soup.find("dt", string="Open to public? ").find_next("dd").string
        opening_times = str(soup.find("dt", string="Opening times:").find_next("dd")).split('<b')[0].lstrip('<dd>').lstrip().split('</dd>')[0]
        special_conditions = soup.find("dt", string="Special conditions:").find_next("dd").string
        facilities = soup.find("dt", string="Facilities:").find_next("dd").string
        public_transportation = soup.find("dt", string="Public transport:").find_next("dd").string
        grid_reference = soup.find("dt", string="Grid ref: ").find_next("dd").string
        size_in_hectares = soup.find("dt", string="Size in hectares:").find_next("dd").string
        fuller_information = soup.find(id='fuller').p.get_text()
        sources_consulted = soup.find("h4", string="Sources consulted:").find_next("p").string



        data = {
            'name': name,
            'summary': summary,
            'previous_name': previous_name,
            'site_location': site_location,
            'postcode': postcode,
            'type_of_site': type_of_site,
            'date': date,
            'designer': designer,
            'listed_structures': listed_structures,
            'borough': borough,
            'site_ownership': site_ownership,
            'site_management': site_management,
            'open_to_public': open_to_public,
            'opening_times': opening_times,
            'special_conditions': special_conditions,
            'facilities': facilities,
            'public_transportation': public_transportation,
            'lon_lat': citymapper_lon_lat,
            'lon': citymapper_lon,
            'lat': citymapper_lat,
            'grid_reference': grid_reference,
            'size_in_hectares': size_in_hectares,
            'image': image_formatted,
            'fuller_information': fuller_information,
            'sources_consulted': sources_consulted,
        }

        data_formatted = {k:(v.rstrip() if isinstance(v, str) else v) for (k,v) in data.items()}
        # print(data_formatted)
        location = Location(**data_formatted)
        location.save()


    def handle(self, *_args, **_options):
        x = urllib.request.urlopen('http://www.londongardensonline.org.uk/search-advanced-results.php?type=%25&keyword=&borough=%25&offset=0')
        soup = BeautifulSoup(x, 'html.parser')

        for link in soup.nav.find_all('a'):
            href = link.get('href')
            print(href)
            href_formatted = href.replace('gardens-online-record.php?','')
            self.scrape_location(href_formatted)
