import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time
from constant import CITIES_LUN
import json
from lun_data_extraction import lun_html_data_extract, lun_json_data_extract
from save_load_functions import save_data_to_csv, save_data_to_json
from dataclasses import asdict
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


json_blocks = []
html_blocks = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }


async def get_raw_page_data(session, sem, url, page_number):
    async with sem:
        minor_url = url + '?page=' + str(page_number)
        async with session.get(minor_url) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            html_object = soup.find_all('div', class_='catalog-card')
            html_blocks.extend(html_object)
            
            script_with_json = soup.find('script', type='application/ld+json').text.strip()
            json_object = json.loads(script_with_json)
            if json_object.get('@type') == "ItemList":
                json_blocks.extend(json_object.get('itemListElement'))
            else:
                nones = [None]*len(html_object)
                json_blocks.extend(nones)


async def gather_all_catalog_links():
    sem = asyncio.Semaphore(3)
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for city in CITIES_LUN:
            for url in (f'https://rieltor.ua/{city}/flats-rent/', f'https://rieltor.ua/{city}/flats-sale/'):
                # url = f'https://rieltor.ua/{city}/flats-rent/'
                async with session.get(url) as response:
                    soup = BeautifulSoup(await response.text(), 'lxml')
                    try:
                        str_total_pages = int(
                            soup.find('ul', class_='pagination_custom').find('li', class_='last').find('a', class_='pager-btn').text.strip()
                            )
                    except Exception:
                        str_total_pages = 1   

                    for page_number in range(1, str_total_pages + 1):
                        task = asyncio.create_task(get_raw_page_data(session, sem, url, page_number))
                        tasks.append(task)
        
            logger.info(f'Finished preparing {city}, estimated {str_total_pages} pages!')
        
        await asyncio.gather(*tasks)


def main(temporary_file_path='lun_real_estate_data'):
    asyncio.run(gather_all_catalog_links())

    cleaned_data = set()  
    for html_object, json_object in zip(html_blocks, json_blocks):
        # data extraction from catalog
        info_dict = lun_json_data_extract(json_object)
        main_info_dict = lun_html_data_extract(html_object)
        
        if info_dict:
            main_info_dict.publication_date = info_dict
        cleaned_data.add(asdict(main_info_dict))
    # save_data_to_csv(cleaned_data, f'{temporary_file_path}.csv')
    save_data_to_json(cleaned_data, f'{temporary_file_path}.json')
    logger.info("Data extraction completed and saved.")
    

if __name__=="__main__":
    logger.info("Scraper is starting to scrape.")
    initial_time = time.time()
    main()
    final_time = time.time() - initial_time
    logger.info(f'Total execution time: {final_time:.2f} seconds')
