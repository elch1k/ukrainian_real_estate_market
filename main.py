from lun_data_parser import main as parser_main
from data_preprocessing import main as preprocessing
from db import main as db_main
import logging
import time


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


if __name__=="__main__":
    temporary_file_path = 'lun_real_estate_data'
    logger.info("Scraper is starting to scrape.")
    initial_time = time.time()
    parser_main(temporary_file_path)
    
    final_time = time.time() - initial_time
    logger.info(f'Total execution time for parsing: {final_time:.2f} seconds')

    preprocessing(temporary_file_path)

    db_main(temporary_file_path)

    # 16 minutes for 40k records