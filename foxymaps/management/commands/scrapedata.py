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
#         links =  [ 'site-record?ID=WST145&sitename=Westminster+Abbey+Precincts+-+The+College+Garden', 'site-record?ID=WST142&sitename=Westminster+Abbey+Precincts+%2F+Westminster+School+-+Dean%27s+Yard', 'site-record?ID=WST146&sitename=Westminster+Cathedral+Piazza', 'site-record?ID=WST147&sitename=Wilton+Crescent+Garden+%2A', 'site-record?ID=WST148&sitename=Wool+House+Garden', 'site-record?ID=WST149&sitename=York+Terrace+West'
# ]
        # for href in links:
        #     print(href)
        #     self.scrape_location(href)
        update_size_error = [
            {
                "id": 76,
                "name": "Moat Mount Open Space and Scratchwood Open Space",
                "href": "site-record?ID=BAR053&sitename=Moat+Mount+Open+Space+and+Scratchwood+Open+Space",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "MM 18.28/Scratchwd 47.96",
                "size_in_hectares_regex": "18.2847.96",
                "size_in_hectares": 47.96
            },
            {
                "id": 81,
                "name": "Oak Hill Park and Oak Hill Woods Local Nature Reserve",
                "href": "site-record?ID=BAR058&sitename=Oak+Hill+Park+and+Oak+Hill+Woods+Local+Nature+Reserve",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "45.51 (woods 5.5)",
                "size_in_hectares_regex": "45.515.5",
                "size_in_hectares": 45.51
            },
            {
                "id": 87,
                "name": "Rowley Green Common",
                "href": "site-record?ID=BAR064&sitename=Rowley+Green+Common",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "9.3 (registered common 8.8)",
                "size_in_hectares_regex": "9.38.8",
                "size_in_hectares": 9.3
            },
            {
                "id": 224,
                "name": "Welsh Harp or Brent Reservoir, Welsh Harp Open Space and Neasden Recreation Ground",
                "href": "site-record?ID=BRE039&sitename=Welsh+Harp+or+Brent+Reservoir%2C+Welsh+Harp+Open+Space+and+Neasden+Recreation+Ground",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "WHR 170; WHOS 9.43; NRG 13.43",
                "size_in_hectares_regex": "1709.4313.43",
                "size_in_hectares": 170
            },
            {
                "id": 240,
                "name": "Broom Hill Common Local Open Space",
                "href": "site-record?ID=BRO013&sitename=Broom+Hill+Common+Local+Open+Space",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "1.75 (0.71 registered common)",
                "size_in_hectares_regex": "1.750.71",
                "size_in_hectares": 1.75
            },
            {
                "id": 269,
                "name": "Husseywell Open Space and The Knoll",
                "href": "site-record?ID=BRO043&sitename=Husseywell+Open+Space+and+The+Knoll",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "2.5 (Husseywell); 4.5 (Knoll)",
                "size_in_hectares_regex": "2.54.5",
                "size_in_hectares": 7
            },
            {
                "id": 272,
                "name": "Keston Common",
                "href": "site-record?ID=BRO046&sitename=Keston+Common",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "55.25 (21.48 registered common",
                "size_in_hectares_regex": "55.2521.48",
                "size_in_hectares": 55
            },
            {
                "id": 298,
                "name": "Spring Park including Cheyne Wood",
                "href": "site-record?ID=BRO087&sitename=Spring+Park+including+Cheyne+Wood",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "20.8 + 1.58 (Cheyne Wood)",
                "size_in_hectares_regex": "20.81.58",
                "size_in_hectares": 20
            },
            {
                "id": 323,
                "name": "Alexandra Road Estate, including Alexandra Road Park",
                "href": "site-record?ID=CAM001&sitename=Alexandra+Road+Estate%2C+including+Alexandra+Road+Park",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "c.6.47 (estate)/1.2434 gardens",
                "size_in_hectares_regex": "6.471.2434",
                "size_in_hectares": 6.5
            },
            {
                "id": 372,
                "name": "Gray's Inn Square and South Square *",
                "href": "site-record?ID=CAM043&sitename=Gray%27s+Inn+Square+and+South+Square+%2A",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "0.3512 Gr. In Sq)/0.2015 S. Sq",
                "size_in_hectares_regex": "0.3512.0.2015.",
                "size_in_hectares": 0.5
            },
            {
                "id": 380,
                "name": "Highgate Cemetery *",
                "href": "site-record?ID=CAM052&sitename=Highgate+Cemetery+%2A",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "East: 7.8177; West: 7.0899",
                "size_in_hectares_regex": "7.81777.0899",
                "size_in_hectares": 14
            },
            {
                "id": 385,
                "name": "Holly Lodge Estate Gardens",
                "href": "site-record?ID=CAM057&sitename=Holly+Lodge+Estate+Gardens",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "1.3911 (estate 24.3)",
                "size_in_hectares_regex": "1.391124.3",
                "size_in_hectares": 24
            },
            {
                "id": 403,
                "name": "Parliament Hill Fields",
                "href": "site-record?ID=CAM074&sitename=Parliament+Hill+Fields",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "(included in Hampstead Heath)",
                "size_in_hectares_regex": "",
                "size_in_hectares": 0.0
            },
            {
                "id": 421,
                "name": "St Benet and All Saints Church Garden",
                "href": "site-record?ID=CAM091&sitename=St+Benet+and+All+Saints+Church+Garden",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "0.0567 (+ 0.0812 private area)",
                "size_in_hectares_regex": "0.05670.0812",
                "size_in_hectares": 0.005
            },
            {
                "id": 427,
                "name": "St John's Churchyard North Extension",
                "href": "site-record?ID=CAM098&sitename=St+John%27s+Churchyard+North+Extension",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "(see St John-at-Hampstead)",
                "size_in_hectares_regex": "",
                "size_in_hectares": 0.0
            },
            {
                "id": 476,
                "name": "Gardens of Middle Temple * (including Fountain Court, Elm Court, Pump Court, Church Court, Brick Court, New Court)",
                "href": "site-record?ID=COL029a&sitename=Gardens+of+Middle+Temple+%2A+%28including+Fountain+Court%2C+Elm+Court%2C+Pump+Court%2C+Church+Court%2C+Brick+Court%2C+New+Court%29",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "MT: 0.484; FC: 0.198",
                "size_in_hectares_regex": "0.4840.198",
                "size_in_hectares": 0.5
            },
            {
                "id": 479,
                "name": "Golden Lane Estate",
                "href": "site-record?ID=COL032&sitename=Golden+Lane+Estate",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "check overall size",
                "size_in_hectares_regex": "",
                "size_in_hectares": 0.0
            },
            {
                "id": 483,
                "name": "Guildhall Piazza and Guildhall Yard",
                "href": "site-record?ID=COL036&sitename=Guildhall+Piazza+and+Guildhall+Yard",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "0.3251 (S) and 0.1868 (N)",
                "size_in_hectares_regex": "0.32510.1868",
                "size_in_hectares": 0.55
            },
            {
                "id": 497,
                "name": "Royal Exchange Buildings",
                "href": "site-record?ID=COL052&sitename=Royal+Exchange+Buildings",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "0.1106 (east) + 0.0773 (west)",
                "size_in_hectares_regex": "0.11060.0773",
                "size_in_hectares": 0.2
            },
            {
                "id": 506,
                "name": "St Andrew Street Garden and Holborn Circus Garden",
                "href": "site-record?ID=COL056a&sitename=St+Andrew+Street+Garden+and+Holborn+Circus+Garden",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "0.0712 + 0.0655",
                "size_in_hectares_regex": "0.07120.0655",
                "size_in_hectares": 0.13
            },
            {
                "id": 512,
                "name": "St Bartholomew-the-Great Churchyard",
                "href": "site-record?ID=COL062&sitename=St+Bartholomew-the-Great+Churchyard",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "0.0744 + 0.0171",
                "size_in_hectares_regex": "0.07440.0171",
                "size_in_hectares": 0.08
            },
            {
                "id": 541,
                "name": "St Nicholas Cole Abbey",
                "href": "site-record?ID=COL091&sitename=St+Nicholas+Cole+Abbey",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "0.0167; 0.0315 adjacent court",
                "size_in_hectares_regex": "0.01670.0315",
                "size_in_hectares": 0.04
            },
            {
                "id": 627,
                "name": "Shirley Heath, including Spring Park Wood",
                "href": "site-record?ID=CRO079&sitename=Shirley+Heath%2C+including+Spring+Park+Wood",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "27.52 + 2.83 (Spring Park Wood",
                "size_in_hectares_regex": "27.522.83",
                "size_in_hectares": 30
            },
            {
                "id": 674,
                "name": "Elthorne Park and Elthorne Waterside",
                "href": "site-record?ID=EAL016&sitename=Elthorne+Park+and+Elthorne+Waterside",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "4.04 (+ extension of 15.32)",
                "size_in_hectares_regex": "4.0415.32",
                "size_in_hectares": 4
            },
            {
                "id": 734,
                "name": "Edmonton Federation Cemetery",
                "href": "site-record?ID=ENF016&sitename=Edmonton+Federation+Cemetery",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "8.1 (with  Western Syn. Cem)",
                "size_in_hectares_regex": "8.1.",
                "size_in_hectares": 8
            },
            {
                "id": 774,
                "name": "Avery Hill Park",
                "href": "site-record?ID=GRN002&sitename=Avery+Hill+Park",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "35.96 inc 7.9 nurseries",
                "size_in_hectares_regex": "35.967.9",
                "size_in_hectares": 42
            },
            {
                "id": 778,
                "name": "Blackheath",
                "href": "site-record?ID=GRN004&sitename=Blackheath",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "121.5 (37.44 in LBG)",
                "size_in_hectares_regex": "121.537.44",
                "size_in_hectares": 121
            },
            {
                "id": 780,
                "name": "Bostall Heath and Bostall Woods",
                "href": "site-record?ID=GRN006&sitename=Bostall+Heath+and+Bostall+Woods",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "Heath 28.95; Woods 36.25",
                "size_in_hectares_regex": "28.9536.25",
                "size_in_hectares": 55
            },
            {
                "id": 789,
                "name": "Cutty Sark Gardens",
                "href": "site-record?ID=GRN015&sitename=Cutty+Sark+Gardens",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "1.07 (Bellot Memorial 0.0486",
                "size_in_hectares_regex": "1.070.0486",
                "size_in_hectares": 1.5
            },
            {
                "id": 796,
                "name": "Eltham Park North, including Shepherdleas Wood",
                "href": "site-record?ID=GRN022&sitename=Eltham+Park+North%2C+including+Shepherdleas+Wood",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "27.08 (inc parkland 6.28)",
                "size_in_hectares_regex": "27.086.28",
                "size_in_hectares": 33
            },
            {
                "id": 826,
                "name": "Shrewsbury Park, including Shrewsbury Tumulus",
                "href": "site-record?ID=GRN061&sitename=Shrewsbury+Park%2C+including+Shrewsbury+Tumulus",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "13.8 + 0.075 (Tumulus)",
                "size_in_hectares_regex": "13.80.075",
                "size_in_hectares": 14
            },
            {
                "id": 846,
                "name": "Woolwich Cemetery (Old and New)",
                "href": "site-record?ID=GRN070&sitename=Woolwich+Cemetery+%28Old+and+New%29",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "c.13.12 (Old 5.14, New 7.98)",
                "size_in_hectares_regex": "13.125.147.98",
                "size_in_hectares": 13
            },
            {
                "id": 881,
                "name": "Millfields Park",
                "href": "site-record?ID=HAC033&sitename=Millfields+Park",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "North: 9.94; South: 14.99",
                "size_in_hectares_regex": "9.9414.99",
                "size_in_hectares": 25
            },
            {
                "id": 886,
                "name": "Shacklewell Green and Shacklewell Lane Triangle",
                "href": "site-record?ID=HAC051&sitename=Shacklewell+Green+and+Shacklewell+Lane+Triangle",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "Green: 0.1/both: 0.27",
                "size_in_hectares_regex": "0.10.27",
                "size_in_hectares": 0.27
            },
            {
                "id": 1012,
                "name": "Lordship Recreation Ground including Model Traffic Area",
                "href": "site-record?ID=HGY023&sitename=Lordship+Recreation+Ground+including+Model+Traffic+Area",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "22.1 (1.83 model traffic area)",
                "size_in_hectares_regex": "22.11.83",
                "size_in_hectares": 22
            },
            {
                "id": 1028,
                "name": "The Grove *",
                "href": "site-record?ID=HGY018&sitename=The+Grove+%2A",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "incl. in  Alexandra Palace",
                "size_in_hectares_regex": ".",
                "size_in_hectares": 0.0
            },
            {
                "id": 1029,
                "name": "Tottenham Cemetery",
                "href": "site-record?ID=HGY039&sitename=Tottenham+Cemetery",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "22.68 (3.2 formal area)",
                "size_in_hectares_regex": "22.683.2",
                "size_in_hectares": 22
            },
            {
                "id": 1159,
                "name": "Stubbers Adventure Centre (including Walled Garden)",
                "href": "site-record?ID=HVG061&sitename=Stubbers+Adventure+Centre+%28including+Walled+Garden%29",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "51.2 (walled garden: 0.3)",
                "size_in_hectares_regex": "51.20.3",
                "size_in_hectares": 51
            },
            {
                "id": 1172,
                "name": "Bessingby Park and Pine Gardens, and Cavendish Recreation Ground",
                "href": "site-record?ID=HIL003&sitename=Bessingby+Park+and+Pine+Gardens%2C+and+Cavendish+Recreation+Ground",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "13.86 (BF: 8.05; SCG 5.80)",
                "size_in_hectares_regex": "13.868.055.80",
                "size_in_hectares": 13
            },
            {
                "id": 1244,
                "name": "Carville Hall Park South",
                "href": "site-record?ID=HOU013&sitename=Carville+Hall+Park+South",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "5.12 (w. Carville Hall North)",
                "size_in_hectares_regex": "5.12.",
                "size_in_hectares": 5
            },
            {
                "id": 1319,
                "name": "Dartmouth Park and Dartmouth Park Hill Reservoirs",
                "href": "site-record?ID=ISL027&sitename=Dartmouth+Park+and+Dartmouth+Park+Hill+Reservoirs",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "2.5 (park 1.09)",
                "size_in_hectares_regex": "2.51.09",
                "size_in_hectares": 2.5
            },
            {
                "id": 1320,
                "name": "Duncan Terrace Garden and Colebrooke Row Gardens",
                "href": "site-record?ID=ISL028&sitename=Duncan+Terrace+Garden+and+Colebrooke+Row+Gardens",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "0.77 (0.47+0.3)",
                "size_in_hectares_regex": "0.770.470.3",
                "size_in_hectares": .8
            },
            {
                "id": 1349,
                "name": "New River Walk including Astey's Row Rock Gardens/Astey's Row Playground",
                "href": "site-record?ID=ISL055&sitename=New+River+Walk+including+Astey%27s+Row+Rock+Gardens%2FAstey%27s+Row+Playground",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "2.09 (1.41+0.68)",
                "size_in_hectares_regex": "2.091.410.68",
                "size_in_hectares": 2
            },
            {
                "id": 1353,
                "name": "Parkland Walk",
                "href": "site-record?ID=ISL059&sitename=Parkland+Walk",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "4.5miles (2.1 in LB Islington)",
                "size_in_hectares_regex": "4.52.1",
                "size_in_hectares": 1
            },
            {
                "id": 1550,
                "name": "Back Green and Malden Green",
                "href": "site-record?ID=KIN004&sitename=Back+Green+and+Malden+Green",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "0.6 (0.3 in RBK)",
                "size_in_hectares_regex": "0.60.3",
                "size_in_hectares": 0.6
            },
            {
                "id": 1640,
                "name": "Rush Common",
                "href": "site-record?ID=LAM037&sitename=Rush+Common",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "3.8 (3.71 Rush Common)",
                "size_in_hectares_regex": "3.83.71",
                "size_in_hectares": 4
            },
            {
                "id": 1654,
                "name": "Streatham Common",
                "href": "site-record?ID=LAM051&sitename=Streatham+Common",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "26.12 (23.93 registered common",
                "size_in_hectares_regex": "26.1223.93",
                "size_in_hectares": 26
            },
            {
                "id": 1675,
                "name": "Brockley Cemetery",
                "href": "site-record?ID=LEW006&sitename=Brockley+Cemetery",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "6.9 (15 with Ladywell Cem.)",
                "size_in_hectares_regex": "6.915.",
                "size_in_hectares": 7
            },
            {
                "id": 1678,
                "name": "Brookmill Park",
                "href": "site-record?ID=LEW009&sitename=Brookmill+Park",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "1.92 (3.6 inc. R.Ravensbourne)",
                "size_in_hectares_regex": "1.923.6.",
                "size_in_hectares": 3.6
            },
            {
                "id": 1763,
                "name": "Pollards Hill Housing Estate, including Donnelly Green and Pollards Hill Recreation Ground",
                "href": "site-record?ID=MER040&sitename=Pollards+Hill+Housing+Estate%2C+including+Donnelly+Green+and+Pollards+Hill+Recreation+Ground",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "1.93 Green/3.42 Rec Ground",
                "size_in_hectares_regex": "1.933.42",
                "size_in_hectares": 5
            },
            {
                "id": 1787,
                "name": "Wimbledon Park (including Wimbledon Golf Course) *",
                "href": "site-record?ID=MER066&sitename=Wimbledon+Park+%28including+Wimbledon+Golf+Course%29+%2A",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "26.95 (+17.65 in LB Merton)",
                "size_in_hectares_regex": "26.9517.65",
                "size_in_hectares": 40
            },
            {
                "id": 1795,
                "name": "City of London Cemetery and Crematorium *",
                "href": "site-record?ID=NEW007&sitename=City+of+London+Cemetery+and+Crematorium+%2A",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "52.65 + 18.63 in reserve",
                "size_in_hectares_regex": "52.6518.63",
                "size_in_hectares": 60
            },
            {
                "id": 1876,
                "name": "Borough Cemetery",
                "href": "site-record?ID=RIC004&sitename=Borough+Cemetery",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "4.05 (12.95 inc reserve land)",
                "size_in_hectares_regex": "4.0512.95",
                "size_in_hectares": 4
            },
            {
                "id": 1930,
                "name": "Palewell Common and Fields",
                "href": "site-record?ID=RIC055&sitename=Palewell+Common+and+Fields",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "14.37 (registered common 5.83)",
                "size_in_hectares_regex": "14.375.83",
                "size_in_hectares": 14
            },
            {
                "id": 1932,
                "name": "Pesthouse Common",
                "href": "site-record?ID=RIC057&sitename=Pesthouse+Common",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "1.18 (0.93 registered common)",
                "size_in_hectares_regex": "1.180.93",
                "size_in_hectares": 1.2
            },
            {
                "id": 2078,
                "name": "Beddington Park and The Grange, including Carew Manor",
                "href": "site-record?ID=SUT004&sitename=Beddington+Park+and+The+Grange%2C+including+Carew+Manor",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "BPk 38.09/RPW 15.47/Gr 17.73",
                "size_in_hectares_regex": "38.0915.4717.73",
                "size_in_hectares": 70
            },
            {
                "id": 2117,
                "name": "Rosehill Park East and Rosehill Park West",
                "href": "site-record?ID=SUT044&sitename=Rosehill+Park+East+and+Rosehill+Park+West",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "East: 12.79. West: 15.47",
                "size_in_hectares_regex": "12.79.15.47",
                "size_in_hectares": 30
            },
            {
                "id": 2274,
                "name": "Walthamstow Town Hall Complex and Chestnuts Sports Ground",
                "href": "site-record?ID=WAL049&sitename=Walthamstow+Town+Hall+Complex+and+Chestnuts+Sports+Ground",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "4.76 Town Hall/3.63 Showground",
                "size_in_hectares_regex": "4.763.63",
                "size_in_hectares": 5
            },
            {
                "id": 2297,
                "name": "Holborn Estate; Diprose Lodge",
                "href": "site-record?ID=WND021&sitename=Holborn+Estate%3B+Diprose+Lodge",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "2.4? (0.96?)",
                "size_in_hectares_regex": "2.40.96",
                "size_in_hectares": 3.5
            },
            {
                "id": 2322,
                "name": "Royal Victoria Patriotic Building Grounds",
                "href": "site-record?ID=WND050&sitename=Royal+Victoria+Patriotic+Building+Grounds",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "(incl. in Wandsworth Common)",
                "size_in_hectares_regex": ".",
                "size_in_hectares": 0.0
            },
            {
                "id": 2335,
                "name": "Tooting Common",
                "href": "site-record?ID=WND063&sitename=Tooting+Common",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "97.6 (T Bec 58.12;  TGr 22.13)",
                "size_in_hectares_regex": "97.658.1222.13",
                "size_in_hectares": 97
            },
            {
                "id": 2338,
                "name": "Wandsworth Common",
                "href": "site-record?ID=WND067&sitename=Wandsworth+Common",
                "size_in_hectares_error": False,
                "size_in_hectares_raw": "71.7 (69.43 registered common)",
                "size_in_hectares_regex": "71.769.43",
                "size_in_hectares": 71
            }
        ]


        for item in update_size_error:
            index_id = Location.objects.get(id=item['id'])
            index_id.size_in_hectares = item['size_in_hectares']
            index_id.save()


        # b = Location.objects.get(id=2489)
        # b.delete()

        # b = Location.objects.filter(size_in_hectares_error=True)
        # print(b)
