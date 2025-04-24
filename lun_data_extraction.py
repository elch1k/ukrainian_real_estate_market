import re
# from constant import CITY_CODE
from flat_dataclass import ApartmentInfo
from datetime import datetime


def manual_converting_price_into_uah(price):
    if "грн/міс" in price or "грн" in price:
        return round(float(''.join(item for item in re.findall(r'\d+', price))), 2), "₴"
    elif "$/міс" in price or "$" in price:
        return round(float(''.join(item for item in re.findall(r'\d+', price))), 2), "$"
    elif "€/міс" in price or "€" in price:
        return round(float(''.join(item for item in re.findall(r'\d+', price))), 2), "€"
    else:
        return None


def lun_json_data_extract(json_object):
    if json_object:
        apartment_info = json_object.get('item')
        date = apartment_info.get('offers').get('availabilityStarts')
        date = date[:-3]
        dt = datetime.strptime(date, "%Y-%m-%d %H:%M")
        date_only = dt.strftime("%Y-%m-%d")
    else:
        date_only = None
    
    return date_only


def lun_html_data_extract(html_object):
    apartment = ApartmentInfo()

    # coordinates
    apartment.latitude = float(html_object.get('data-latitude')) if len(html_object.get('data-latitude')) > 0 else None
    apartment.longitude = float(html_object.get('data-longitude')) if len(html_object.get('data-longitude')) > 0 else None
    
    # total number of photos and first 5 photos for user
    photos_section = html_object.find('div', class_='catalog-card-images').find('div', class_='offer-photo-slider-slides-container')
    photos_section = photos_section.find_all('div', class_='offer-photo-slider-slide')
    # apartment.top5_photos = [photo.find('img', class_='offer-photo-slider-slide-image').get('src') for photo in photos_section[:5]]
    apartment.photo_count = len(photos_section)

    # price section
    price = html_object.find('div', class_='catalog-card-price').find('strong', class_='catalog-card-price-title').text.strip()    
    apartment.price, apartment.currency = manual_converting_price_into_uah(price)

    # address section
    address_block = html_object.find('h2').find('a', {'data-analytics-event': 'card-click-geo_title'})
    apartment.url = address_block.get('href')
    if 'rent' in apartment.url:
        apartment.deal_type = 'Rent'
    else:
        apartment.deal_type = 'Sale'
    
    address = address_block.find('div', class_='catalog-card-address').text.strip()
    apartment.street_name = address.split(', ')[0]

    # flat location
    location_data = html_object.find('div', class_='catalog-card-region')
    location_data = location_data.find_all('a', {'data-analytics-event': 'card-click-region'})
    apartment.city = location_data[0].text.strip()  # CITY_CODE.get(location_data[0].text.strip())
    if len(location_data) > 1:
        apartment.main_area = location_data[1].text.strip()[:-4]
    else:
        None

    # other details
    card_details_row = html_object.find_all('div', class_='catalog-card-details-row')
    rooms_info = card_details_row[0].find('span', class_='').text.strip()
    pattern = r'\d+'
    apartment.room = int(re.search(pattern, rooms_info).group()) if re.search(pattern, rooms_info) else None
    
    squares_info = card_details_row[1].find('span', class_='').text.strip()[:-3]
    squares_info = squares_info.split(' / ')
    apartment.total_square = float(squares_info[0])
    apartment.living_square = float(squares_info[1])
    apartment.kitchen_square = float(squares_info[2])

    floors_info = card_details_row[2].find('span', class_='').text.strip()
    pattern = r'\d+'
    floors_info = re.findall(pattern, floors_info)
    apartment.total_floor = int(floors_info[1])
    apartment.flat_floor = int(floors_info[0])


    card_info = html_object.find('div', class_='catalog-card-chips')
    subway = card_info.find('a', {'data-analytics-event': 'card-click-subway_chip'})
    if subway:
        apartment.subway = True if subway.find('span').text.strip() else False
    
    newbuild = card_info.find('a', {'data-analytics-event': 'card-click-newhouse_chip'})
    if newbuild:
        apartment.newbuild_name = newbuild.text.strip()
    
    animal = card_info.find_all('a', {'data-analytics-event': 'card-click-allow_pets_chip'})
    if len(animal) > 0:
        if len(animal) > 1:
            apartment.animal = True
        elif len(animal) == 1 and (animal[0].text.strip().lower() == "можна з тваринами" or animal[0].text.strip().lower() == "можна з деякими тваринами"):
            apartment.animal = True
    
    second_district = card_info.find('a', {'data-analytics-event': 'card-click-landmark_chip'})
    if second_district:
        apartment.second_area = second_district.text.strip()
    
    description_block = html_object.find('div', class_="catalog-card-description")
    if description_block:
        apartment.description = description_block.find('span', {'style': '-webkit-box-orient: vertical'}).text.replace('\n', ' ').strip()

    catalog_card_author = html_object.find('div', class_='catalog-card-author')
    
    verified = catalog_card_author.find('div', class_='catalog-card-author-verification')
    if verified:
        apartment.checked_apartment = True if verified.get('title') == "Верифікований профіль" else False

    agency = catalog_card_author.find('div', class_='catalog-card-author-content').find('div', class_='catalog-card-author-company')
    if agency:
        apartment.agency_name = agency.find('button', {'data-analytics-event': 'card-click-agency_name'}).text.strip()

    apartment.parse_date = str(datetime.today().date())


    return apartment