# run.py
from my_scraper.scraper import TenderScraper
from config.settings import WEBDRIVER_PATH

if __name__ == "__main__":
    # Create an instance of the TenderScraper class
    scraper = TenderScraper(WEBDRIVER_PATH)

    # Specify the URLs for scraping
    world_bank_url = "https://www.example.com/world_bank"
    chinese_tenders_url = "https://www.example.com/chinese_tenders"

    # Call the respective methods for scraping
    scraper.scrape_world_bank(world_bank_url)
    scraper.scrape_chinese_tenders(chinese_tenders_url)

    # Close the browser after scraping
    scraper.close_browser()
