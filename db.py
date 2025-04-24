from sqlalchemy import create_engine, URL
from sqlalchemy.orm import  sessionmaker
from model import City, MainArea, SecondArea, Agency, Apartment, StatTable, Street, Newbuild, DealType, Currency
from collections import defaultdict
import datetime
from save_load_functions import load_json_file
import logging
from sqlalchemy import select


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def make_db_session(drivername="postgresql+psycopg2",
                    username="postgres",
                    password="dmytro21",
                    host="localhost",
                    database="apartment_db"):
    url_object = URL.create(
        drivername=drivername,
        username=username,
        password=password,
        host=host,       
        database=database
    )
    engine = create_engine(url_object, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


# def get_id_from_cache_or_add_new(key, cache, object_class, session, **kwargs):
#     if key and key not in cache:
#         new_item = object_class(**kwargs)
#         session.add(new_item)
#         session.flush()
#         cache[key] = new_item.id
#         logger.debug(f"Added new item: {key}")
#     item_id = cache.get(key)
#     return item_id


def update_database(session, new_data=None):
    if not new_data:
        logger.error('New data file is empty')
        return
    
    try:
        city_cache = {row.name: row.id for row in session.execute(select(City.name, City.id)).all()}
        currency_cache = {row.symbol: row.id for row in session.execute(select(Currency.symbol, Currency.id)).all()}
        deal_type_cache = {row.name: row.id for row in session.execute(select(DealType.name, DealType.id)).all()}
        main_area_cache = {(row.city_id, row.name): row.id for row in session.execute(select(MainArea.city_id, MainArea.name, MainArea.id)).all()}
        second_area_cache = {(row.city_id, row.name): row.id for row in session.execute(select(SecondArea.city_id, SecondArea.name, SecondArea.id)).all()}
        street_cache = {(row.city_id, row.name): row.id for row in session.execute(select(Street.city_id, Street.name, Street.id)).all()}
        newbuild_cache = {(row.city_id, row.name): row.id for row in session.execute(select(Newbuild.city_id, Newbuild.name, Newbuild.id)).all()}
        agency_cache = {(row.city_id, row.name): row.id for row in session.execute(select(Agency.city_id, Agency.name, Agency.id)).all()}
        # print(city_cache)

        city_count = defaultdict(int)
        new_records = []
        updated_records = []
        
        for row in new_data:
            url = row.get('url')
            if not url:
                logger.info("Missing URL")
                continue
            
            if (not row.get('latitude')) or (not row.get('longitude')) or (not row.get('price')):
                continue

            city_name = row.get('city')
            if not city_name:
                logger.info("Missing city")
                continue

            if city_name not in city_cache:
                new_city = City(name=city_name)
                session.add(new_city)
                session.flush()
                city_cache[city_name] = new_city.id
                logger.debug(f"Added new city: {city_name}")

            city_id = city_cache[city_name]
            city_count[city_id]+=1
            
            existing_record = session.execute(select(Apartment).where(Apartment.url==url)).scalar_one_or_none()
            if existing_record:
                potential_new_price = row.get('price')
                if potential_new_price is not None and existing_record.price != potential_new_price:
                    existing_record.price = potential_new_price
                    updated_records.append(existing_record)
                    logger.debug(f"Updated price for listing: {url}")
                continue

            currency_symbol = row.get('currency')
            if currency_symbol and currency_symbol not in currency_cache:
                new_currency = Currency(symbol=currency_symbol)
                session.add(new_currency)
                session.flush()
                currency_cache[currency_symbol] = new_currency.id
                logger.debug(f"Added new currency: {currency_symbol}")
            currency_id = currency_cache.get(currency_symbol)

            deal_type_name = row.get('deal_type')
            if deal_type_name and deal_type_name not in deal_type_cache:
                new_deal_type = DealType(name=deal_type_name)
                session.add(new_deal_type)
                session.flush()
                deal_type_cache[deal_type_name] = new_deal_type.id
                logger.debug(f"Added new deal type: {deal_type_name}")
            deal_type_id = deal_type_cache.get(deal_type_name)

            main_area_name = row.get('main_area')
            if main_area_name and (city_id, main_area_name) not in main_area_cache:
                new_main_area = MainArea(city_id=city_id, name=main_area_name)
                session.add(new_main_area)
                session.flush()
                main_area_cache[(city_id, main_area_name)] = new_main_area.id
                logger.debug(f"Added new main area: {main_area_name}")
            main_area_id = main_area_cache.get((city_id, main_area_name))

            second_area_name = row.get('second_area')
            if second_area_name and (city_id, second_area_name) not in second_area_cache:
                new_second_area = SecondArea(city_id=city_id, name=second_area_name)
                session.add(new_second_area)
                session.flush()
                second_area_cache[(city_id, second_area_name)] = new_second_area.id
                logger.debug(f"Added new second area: {second_area_name}")
            second_area_id = second_area_cache.get((city_id, second_area_name))

            street_name = row.get('street_name')
            if street_name and (city_id, street_name) not in street_cache:
                new_street = Street(city_id=city_id, name=street_name)
                session.add(new_street)
                session.flush()
                street_cache[(city_id, street_name)] = new_street.id
                logger.debug(f"Added new street: {street_name}")
            street_id = street_cache.get((city_id, street_name))            

            agency_name = row.get('agency_name')
            if agency_name and (city_id, agency_name) not in agency_cache:
                new_agency = Agency(city_id=city_id, name=agency_name)
                session.add(new_agency)
                session.flush()
                agency_cache[(city_id, agency_name)] = new_agency.id
                logger.debug(f"Added new agency: {agency_name}")
            agency_id = agency_cache.get((city_id, agency_name))

            newbuild_name = row.get('newbuild_name')
            if newbuild_name and (city_id, newbuild_name) not in newbuild_cache:
                new_newbuild = Newbuild(city_id=city_id, name=newbuild_name)
                session.add(new_newbuild)
                session.flush()
                newbuild_cache[(city_id, newbuild_name)] = new_newbuild.id
                logger.debug(f"Added new newbuild: {newbuild_name}")
            newbuild_id = newbuild_cache.get((city_id, newbuild_name))               
            
            new_record = Apartment(
                price=row.get('price'),
                currency_id=currency_id,
                city_id=city_id,
                main_area_id=main_area_id,
                second_area_id=second_area_id,
                street_id=street_id,
                subway=row.get('subway'),
                total_square=row.get('total_square'),
                kitchen_square=row.get('kitchen_square'),
                living_square=row.get('living_square'),
                room=row.get('room'),
                total_floor=row.get('total_floor'),
                flat_floor=row.get('flat_floor'),
                deal_type_id=deal_type_id,
                checked_apartment=row.get('checked_apartment'),
                animal=row.get('animal'),                    
                newbuild_id=newbuild_id,
                agency_id=agency_id,
                photo_count=row.get('photo_count'),
                latitude=row.get('latitude'),
                longitude=row.get('longitude'),
                url=row.get('url'),                    
                publication_date=row.get('publication_date'),                    
                parse_date=row.get('scraped_date'),
                description=row.get('description'),                    
                is_active=row.get('is_active'),
                no_active_date=row.get('no_active_date')
            )

            new_records.append(new_record)

        if new_records:
            session.add_all(new_records)
            logger.info(f"Added {len(new_records)} new listings")
        
        new_urls = {row.get('url') for row in new_data if row.get('url')}
        inactive_records = session.execute(
            select(Apartment).where(Apartment.url.not_in(new_urls), Apartment.is_active == True)
            ).scalars().all()

        for record in inactive_records:
            record.is_active = False
            record.no_active_date = datetime.date.today()
            updated_records.append(record)

        date_parse = datetime.date.today()
        stat_records = [StatTable(city_id=city_id, parse_date=date_parse, num_ads=count)
            for city_id, count in city_count.items()]
        if stat_records:
            session.add_all(stat_records)
            logger.info(f"Added {len(stat_records)} statistics records")
        
        session.commit()
        logger.info(f"Database updated: {len(new_records)} inserted, {len(updated_records)} updated, {len(stat_records)} stats added")
    except Exception as e:
        session.rollback()
        logger.info(f'Error during DB update: {e}')


def main(temporary_file_path='lun_real_estate_data'):
    session = make_db_session()
    all_data = load_json_file(f'{temporary_file_path}.json')
    update_database(new_data=all_data, session=session)
    
    logger.info('Finished work!')


if __name__=='__main__':
    logger.info('Start add info into DB')
    main(temporary_file_path='lun_real_estate_data')