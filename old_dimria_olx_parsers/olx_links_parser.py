import aiohttp
import asyncio
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Optional
import time
import logging
from constant import CITIES_OLX, CITY_AREA_OLX
from save_load_functions import save_data_to_csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class QuickInformation:
    city: Optional[str] = None
    main_area: Optional[str] = None
    url: Optional[str] = None

announcement_links = []
# need manually change
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}

async def get_raw_page_data(session: aiohttp.ClientSession, sem: asyncio.Semaphore, url: str, page_number: int):
    async with sem:
        minor_url = url + '&page=' + str(page_number)
        try:
            async with session.get(minor_url) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                full_page_block = soup.find('div', class_="listing-grid-container css-d4ctjd")
                catalog_blocks = full_page_block.find_all('div', class_='css-1apmciz')
                announcements = []
                for block in catalog_blocks:
                    href = block.find('a', class_='css-qo0cxu').get('href')
                    location_date_data = block.find('div', class_='css-odp1qd').find('p', {'data-testid': 'location-date'})
                    
                    if location_date_data:
                        location_data = location_date_data.text.strip().split(' - ')[0]
                        city, main_area = location_data.split(', ')
                    announcements.append(QuickInformation(city=city, main_area=main_area, url=f'https://www.olx.ua/{href}'))
                return announcements
        except Exception as e:
            logger.error(f"Error fetching data from {minor_url}: {e}")
            return []


async def gather_all_catalog_links():
    sem = asyncio.Semaphore(3)
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for city in CITIES_OLX:
            city_area_ids = CITY_AREA_OLX.get(city, [])
            for area_id in city_area_ids:
                url = f'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/{city}/?currency=UAH&search%5Bdistrict_id%5D={area_id}'
                async with session.get(url) as response:
                    soup = BeautifulSoup(await response.text(), 'lxml')
                    try:
                        page_panel = soup.find('div', {'data-testid':'pagination-wrapper'}).find('ul', {'data-testid': 'pagination-list'})
                    except Exception:
                        str_total_pages = 1   
                    else:   
                        str_total_pages = int(page_panel.find_all('li', {'data-testid': 'pagination-list-item'})[-1].find('a', class_='css-1mi714g').text.strip())

                    for page_number in range(1, str_total_pages + 1):
                        task = asyncio.create_task(get_raw_page_data(session, sem, url, page_number))
                        tasks.append(task)
                        await asyncio.sleep(0.5)
        
        results = await asyncio.gather(*tasks)
        return [announcement for sublist in results for announcement in sublist]

def main():
    initial_time = time.time()
    announcement_links = asyncio.run(gather_all_catalog_links())
    save_data_to_csv(announcement_links, 'olx_announcement_urls.csv')
    final_time = time.time() - initial_time
    logger.info(f"Execution time: {final_time} seconds")
    

if __name__=="__main__":
    main()