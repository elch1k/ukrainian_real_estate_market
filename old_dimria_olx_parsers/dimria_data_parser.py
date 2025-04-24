import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time
from constant import CITIES_DIMRIA
import json
from save_load_functions import save_data_to_csv
from dimria_data_extraction import dimria_json_data_extract

blocks = []

async def get_raw_page_data(session, sem, url, page_number):
    async with sem:
        # define url of catalog page
        minor_url = url + '?page=' + str(page_number)
        
        async with session.get(minor_url) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            script_with_json = soup.find_all('script')[2].text.strip()[25:-122]
            json_object = json.loads(script_with_json)
            blocks.extend(json_object.get('catalog', {}).get('realtyForCatalog', []))


async def gather_all_catalog_links():
    sem = asyncio.Semaphore(4)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for city in CITIES_DIMRIA:
            url = f"https://dom.ria.com/uk/arenda-kvartir/{city}/"
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(), "lxml")
                try:
                    page_panel = soup.find('span', class_='pagerMobileScroll')
                except Exception:
                    str_total_pages = 1   
                else:   
                    str_total_pages = int(page_panel.find_all('a', class_='page-item button-border')[-1].text.strip())

                for page_number in range(1, str_total_pages + 1):
                    task = asyncio.create_task(get_raw_page_data(session, sem, url, page_number))
                    tasks.append(task)
                
        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_all_catalog_links())

    cleaned_data = []
    for data in blocks:
        cleaned_data.append(dimria_json_data_extract(data))

    save_data_to_csv(cleaned_data)


if __name__=="__main__":
    main()