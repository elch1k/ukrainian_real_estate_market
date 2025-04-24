from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import re
import asyncio
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
import logging
from constant import usd_to_uah, eur_to_uah
from save_load_functions import save_data_to_csv
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
}

@dataclass
class ApartmentInfo:
    price_UAH: Optional[float] = None
    city: Optional[str] = None
    main_area: Optional[str] = None
    second_area: Optional[str] = None
    street_name: Optional[str] = None
    subway: bool = False
    total_square: Optional[float] = None
    kitchen_square: Optional[float] = None
    living_square: Optional[float] = None
    rooms: Optional[int] = None
    total_floors: Optional[int] = None
    flat_floor: Optional[int] = None
    wall_type: Optional[str] = None
    checked_apartment: Optional[bool] = None
    newbuild_name: Optional[str] = None
    animal: bool = False
    photo_counts: Optional[int] = None
    top5_photos: List[str] = field(default_factory=list)
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    date: Optional[str] = None
    url: Optional[str] = None


def parse_price(price_str: str) -> Optional[float]:
    try:
        value = float(re.sub(r"[^\d.]", "", price_str))
        if 'грн' in price_str:
            return value
        if '$' in price_str:
            return value * usd_to_uah
        if '€' in price_str:
            return value * eur_to_uah
        return None
    except (ValueError, TypeError):
        return None

async def parse_apartment_data(soup: BeautifulSoup, url: str, city: str, main_area: str) -> ApartmentInfo:
    apartment = ApartmentInfo(url=url, city=city, main_area=main_area)

    # photo section
    swiper = soup.find('div', class_='swiper')
    if swiper:
        photos = swiper.find_all('div', class_='swiper-slide')
        apartment.photo_counts = len(photos)
        all_photos = swiper.find('div', class_='swiper-wrapper').find_all('div', class_='swiper-slide css-1915wzc')
        apartment.top5_photos = [photo.find('div', class_='swiper-zoom-container').find('img').get('src') for photo in all_photos[:5]]
        
    # price section
    price_container = soup.find('div', {'data-testid': 'ad-price-container'})
    if price_container:
        price_text = price_container.text.strip()
        apartment.price_UAH = parse_price(price_text)

    # main info
    pattern = r'\d+'
    main_section = soup.find('div', class_='css-1wws9er')
    
    if main_section:
        info_items = main_section.find_all('div', class_='css-ae1s7g')
        for item in info_items:
            text = item.text.strip()
            
            if 'Поверх:' in text:
                apartment.flat_floor = int(re.search(pattern, text).group()) if re.search(pattern, text) else None
            elif 'Поверховість:' in text:
                apartment.total_floors = int(re.search(pattern, text).group()) if re.search(pattern, text) else None
            elif 'Загальна площа:' in text:
                apartment.total_square = int(re.search(pattern, text).group()) if re.search(pattern, text) else None
            elif 'Площа кухні:' in text:
                apartment.kitchen_square = int(re.search(pattern, text).group()) if re.search(pattern, text) else None
            elif 'Тип стін' in text:
                apartment.wall_type = text.split(': ')[-1]
            elif 'Кількість кімнат:' in text:
                apartment.rooms = int(re.search(pattern, text).group()) if re.search(pattern, text) else None
            elif ('домашні улюбленці:' and 'так') in text.lower():
                apartment.animal = True
            elif ('Інфраструктура' and 'метро') in text.lower():
                apartment.subway = True

        # description section
        main_description = main_section.find('div', {'data-testid': 'ad_description'})
        if main_description:
            apartment.description = main_description.text.strip().replace("\n", "")
    
    return apartment

async def process_url(session: aiohttp.ClientSession, sem: asyncio.Semaphore, url: str, city: str, main_area: str) -> Optional[ApartmentInfo]:
    async with sem:       
        async with session.get(url) as response:     
            soup = BeautifulSoup(await response.text(), 'lxml')
            return await parse_apartment_data(soup, url, city, main_area)


async def gather_apartment_data(file_path: str) -> List[ApartmentInfo]:
    sem = asyncio.Semaphore(4)
    
    try:
        df = pd.read_csv(file_path, usecols=['url', 'city', 'main_area'])
        df = df[:10]  # TEST!!!
    except Exception as e:
        logger.error(f"Failed to read CSV: {e}")
        return []

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [process_url(session, sem, row.url, row.city, row.main_area) for row in df.itertuples()]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result]


def main():
    start_time = time.time()
    
    try:
        data = asyncio.run(gather_apartment_data("olx_announcement_urls.csv"))
        save_data_to_csv(data, "olx_real_estate.csv")
    except Exception as e:
        logger.error(f"Main execution failed: {e}")
    
    final_time = time.time() - start_time
    logger.info(f"Execution completed in {final_time:.2f} seconds")

if __name__ == "__main__":
    main()