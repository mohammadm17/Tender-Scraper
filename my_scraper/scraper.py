import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import os
import shutil

class TenderScraper:
    def __init__(self, webdriver_path):
        self.driver = webdriver.Firefox(executable_path=webdriver_path)
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(filename='log_file_world_bank.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def close_browser(self):
        self.driver.quit()

    def download_file(self, link_xpath, destination_folder):
        try:
            # Find the download link
            download_link = self.driver.find_element(By.XPATH, link_xpath)

            # Get the file name from the download link
            file_name = download_link.get_attribute("href").split("/")[-1]

            # Click the download link
            download_link.click()

            # Wait for the download to complete (you may need to adjust the sleep time)
            time.sleep(10)  # Adjust as needed based on file size and network speed

            # Move the downloaded file to the specified destination folder
            source_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)
            destination_path = os.path.join(destination_folder, file_name)
            shutil.move(source_path, destination_path)

            logging.info(f"Successfully downloaded and saved {file_name} to {destination_folder}")
            return True
        except Exception as e:
            logging.error(f"Error downloading file: {str(e)}")
            return False

    def scrape_world_bank(self, webpage_url, destination_folder):
        logging.basicConfig(filename='log_file_world_bank.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        try:
            self.driver.get(webpage_url)
            time.sleep(5)

            # Download the first file
            if self.download_file('/html/body/div[1]/div/div[4]/div/section/div/section[1]/div/div/div/div/div/div[2]/div/table/tbody/tr[1]/td[3]/h4/a', destination_folder):
                logging.info("Successfully downloaded First file")

            # Switch back to the main window
            self.driver.switch_to.window(self.driver.window_handles[0])

            # Download the second file
            if self.download_file('/html/body/div[1]/div/div/4/div/section/div/section[1]/div/div/div/div/div/div[2]/div/table/tbody/tr[2]/td[3]/h4/a', destination_folder):
                logging.info("Successfully downloaded Second file")

        except Exception as e:
            logging.error(str(e))
        finally:
            self.driver.quit()

    def scrape_chinese_tenders(self, webpage_url):
        try:
            self.driver.get(webpage_url)
            

            time.sleep(7)
            tender2 = (self.driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div[1]/div[1]/div/div/span[2]/a").click())

            window_handles = self.driver.window_handles
            self.driver.switch_to.window(window_handles[1])
            time.sleep(5)
            tender_All = self.driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/div[2]/form/div/ul/li[1]/div/ul/li[2]")
            time.sleep(5)
            tender_All.click()
            bid_link= []
            newlist = []
            a = []
            m = 10
            tender_type = []
            tender_procurement_no = []
            Date = []
            regions = []
            industries = []


            for i in range(0,10):
                newlist = []
                for final_text in self.driver.find_elements(By.XPATH, "/html/body/div/div/div[3]/div/div[3]/ul"):
                    newlist.append(final_text.text)
                a = []
                for new_list in newlist:
                    a.append(new_list.split("\n"))
              
                logging.info("Fetching Tenders")


                for  procurement in a[0][::5]:
                    pattern_procurement = r'\d{4}-\w{12,15}'
                    match = re.search(pattern_procurement, procurement)

                    if match:
                        extracted_portion = match.group(0)
                        tender_procurement_no.append(extracted_portion)
                for tendertype in a[0][1::5]:
                    tender_type.append(tendertype)

                for text in a[0][2::5]:
                    pattern_date = r'\d{4}-\d{2}-\d{2}'
                    match = re.search(pattern_date, text)
                    if match:
                        date = match.group(0)
                        Date.append(date)

                for industry1 in a[0][4::5]:
                    pattern = r'Industry：(.*?) Region：(.*?)$'
                    match = re.search(pattern, industry1)
                    if match:
                        industry = match.group(1)
                        region = match.group(2)
                        industries.append(industry)
                        regions.append(region)



                for button231 in soup.find_all('a', href=True):
                    if button231['href'] == 'javascript:void(0);':
                        pass
                    else:
                        bid_link.append(button231['href'])
                time.sleep(5)
                next_page = self.driver.find_element(By.XPATH, f"/html/body/div/div/div[3]/div/div[4]/div/div/ul/form/li[{m}]/a")

                if i < 5:
                    m = 10
                else:
                    m = 11

                time.sleep(5)

                next_page.click()
                logging.info("Fetching NExt PAge")
                time.sleep(10)
        except Exception as e:
            logging.error(str(e))
        finally:
            self.driver.quit()
            self.save_data_to_csv("chinese_tenders_data.csv")        

    def scrape_international_chinese_tenders(self, webpage_url):
        logging.basicConfig(filename='log_file_chinese_international.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    
    # Set up the Selenium webdriver (Firefox)
    
    
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        try:
            # Open the webpage in the browser
            self.driver.get(webpage_url)


            More_tenders = (self.driver.find_element(By.XPATH, "/html/body/section/div/div[3]/div[1]/div/p/a").click())

            window_handles = self.driver.window_handles
            self.driver.switch_to.window(window_handles[1])
            time.sleep(10)
            international_list = []
            international_data = []
            tender_type = []
            tender_procurement_no = []
            Date = []
            regions = []
            industries = []
            Project_Description = []
            tender_All = self.driver.find_element(By.XPATH, "/html/body/section/div/div[2]/form/div/div[1]/div[2]/span[1]")

            tender_All.click()
            time.sleep(10)
            for i in range(0,5):

                for final_text in self.driver.find_elements(By.XPATH, '//*[@id="infoList"]'):
                    international_list.append(final_text.text)

                for new_list in international_list:
                    international_data.append(new_list.split("\n"))

                for  procurement in international_data[0][::5]:
                                pattern_procurement = r'\d{4}-\w{12,15}'
                                match = re.search(pattern_procurement, procurement)

                                if match:
                                    extracted_portion = match.group(0)
                                    tender_procurement_no.append(extracted_portion)
                time.sleep(10)

                for tendertype in international_data[0][1::5]:
                            tender_type.append(tendertype)

                for text in international_data[0][2::5]:
                            pattern_date = r'\d{2}-\d{2}-\d{4}'
                            match = re.search(pattern_date, text)
                            if match:
                                date = match.group(0)
                                Date.append(date)
                for project_descrpt in international_data[0][3::5]:
                    Project_Description.append(project_descrpt)

                for item in international_data[0][4::5]:
                    industry_match = re.search(r'Industry:(.*?)Region:', item)
                    region_match = re.search(r'Region:(.*?)source:', item)

                    if industry_match:
                        industry = industry_match.group(1).strip()
                        industries.append(industry)

                    if region_match:
                        region = region_match.group(1).strip()
                        regions.append(region)
                next_page = driver.find_element(By.XPATH, '//*[@id="next"]')


                time.sleep(5)

                next_page.click()
                        #logging.info("Fetching NExt PAge")
                time.sleep(10)





                logging.info("Fetching NExt PAge")



        except Exception as e:
            logging.error(str(e))

        finally:
            # Close the browser
            self.driver.quit()
            try:
                data = {
                    'Tender Procurement Number': tender_procurement_no,
                    'Tender Type': tender_type,
                    'Date': Date,
                    'Industry': industries,
                    'Region': regions,
                    "Project Description" : Project_Description
                 }
                logging.info(len(tender_procurement_no))
                logging.info(len(tender_type))
                logging.info(len(Date))
                logging.info(len(industries))
                df = pd.DataFrame(data)
          # Save DataFrame to a CSV file
                csv_filename = 'tender_chinese_international_data.csv'
                df.to_csv(csv_filename, index=False)
                logging.info("Scraping completed")

            except Exception as e:
                logging.error(str(e))
        
        
    def scrape_cppc_org(self, webpage_url):
        logging.basicConfig(filename='log_file_cppc.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        try:
            # Open the webpage in the browser
            self.driver.get(webpage_url)
            cppc_list,cppc_data = [],[]
            for cppc in self.driver.find_elements(By.XPATH, '/html/body/div[4]/div[1]/div/ul'):
                            cppc_list.append(cppc.text)
            for cppc_1 in cppc_list:
                            cppc_data.append(cppc_1.split("\n"))
            project_head = cppc_data[0][0::2]
            project_descript = cppc_data[0][1::2]
            data ={"Project" : project_head,
                  "Project Description" : project_descript}

            df1 = pd.DataFrame(data)
            csv_filename = 'cppc_data.csv'
            df1.to_csv(csv_filename, index=False)
            logging.info(f"Successfully Scraped the website:{webpage_url}")
            scraping = 'Completed Successfully'
        except Exception as e:
            logging.error(str(e))
            scraping = "Not Completed Successfully"
        finally:
            driver.quit()
            logging.info(f"Scraping status: {scraping}")

    def scrape_indian_tender(self, webpage_url):
        logging.basicConfig(filename='log_file_indian_tender.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        try:
            # Open the webpage in the browser
            self.driver.get(webpage_url)
            indian = pd.read_html(url5)
            data_indian = {'Tender Title': indian[11][0],
            'Reference No': indian[11][1],
            'Closing Date':indian[11][2],
            'Bid Opening Date':indian[11][3]}
            df1 = pd.DataFrame(data_indian)
            csv_filename = 'India_data.csv'
            df1.to_csv(csv_filename, index=False)
            data2 = {indian[13][0][0]: indian[14][0],
                     indian[13][1][0]: indian[14][1],
                     indian[13][2][0]: indian[14][2],
                     indian[13][3][0]: indian[14][3]
                    }
            df2 = pd.DataFrame(data_corringdeum)
            csv_filename2 = "Indian_Corrigendum.csv"
            df2.to_csv(csv_filename2, index=False)
        except Exception as e:
            logging.error(str(e))

        finally:
            self.driver.quit()
            logging.info("Scraping Completed")


if __name__ == "__main__":
    # Specify the path to the WebDriver executable
    webdriver_path = GeckoDriverManager().install()

    # Create an instance of the TenderScraper class
    scraper = TenderScraper(webdriver_path)

    # Specify the URL for scraping
    world_bank_url = "https://www.example.com/world_bank"
    international_chinese_tenders_url = "https://www.chinabidding.com/en"
    cppc_org_url = "https://www.cpppc.org/en/PPPyd.jhtml"
    indian_tender_url = 'https://etenders.gov.in/eprocure/app'
    chinese_tender_url = 'https://www.chinabidding.com/en'
    # Specify the destination folder where you want to save the downloaded files
    destination_folder = "D:\Ineuron"

    # Call the scrape_world_bank method
    scraper.scrape_world_bank(world_bank_url, destination_folder)
    scraper.scrape_international_chinese_tenders(international_chinese_tenders_url)
    scraper.scrape_cppc_org(cppc_org_url)
    scraper.scrape_indian_tender(indian_tender_url)
    # Close the browser after scraping
    scraper.close_browser()
