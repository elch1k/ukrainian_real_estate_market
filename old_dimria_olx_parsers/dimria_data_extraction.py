def dimria_json_data_extract(data):
    uah_price = data.get('priceUAH')

    # squares
    total_square = data.get('total_square_meters')
    kitchen_square = data.get('kitchen_square_meters')
    living_square = data.get('living_square_meters')

    total_floors = data.get('floors_count')
    flat_floor = data.get('floor')
    rooms = data.get('rooms_count')

    # location
    street = data.get('street_name_uk')
    city, main_district, second_district, metro = None, None, None, None
    geo_blocks = data.get('cardRelink', [])
    for block in reversed(geo_blocks):
        if block.get('type') == 'city':
            city = block.get('anchor')
        elif block.get('type') == 'area' and main_district == None:
            main_district = block.get('anchor')
        elif block.get('type') == 'area' and main_district != None:
            second_district = block.get('anchor')
        elif block.get('type') == 'metro':
            metro = block.get('anchor')

    top5_photos = []
    photos = data.get('photos')
    for photo in photos:
        photo_file = photo.get('file')
        photo_file = 'https://cdn.riastatic.com/photos/' + photo_file.split('.')[0] + 'b.jpg'
        top5_photos.append(photo_file)

    wall_type = data.get('wall_type')
    description = data.get('description_uk') or data.get('description')
    newbuild_name = data.get('user_newbuild_name_uk')
    animal = data.get("withAnimal")
    checked_apartment = True if data.get("video_inspected") else False

    photo_counts = data.get('photos_count')
    latitude = data.get('latitude')    # latitude first / longitude second
    longitude = data.get('longitude')

    date = data.get('publishing_date')
    url = 'https://dom.ria.com/uk/' + str(data.get('beautiful_url'))

    return {'price_UAH': uah_price,
            'city': city,
            'main_area': main_district,
            'second_area': second_district,
            'street_name': street,
            'subway': metro,
            'total_square': total_square,
            'kitchen_square': kitchen_square,
            'living_square': living_square,
            'rooms': rooms,
            'total_floors': total_floors,
            'flat_floor': flat_floor,
            'wall_type': wall_type,
            'checked_apartment': checked_apartment,
            'newbuild_name': newbuild_name,
            'animal': animal,
            'photo_counts': photo_counts,
            'description': description,
            'latitude': latitude,
            'longitude': longitude,
            'date': date,
            'url': url}