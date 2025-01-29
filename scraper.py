from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

class BillerOperatingUnitScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed
        self.url = "https://www.bharat-connect.com/statistics/biller-operating-units/"
        self.wait = WebDriverWait(self.driver, 10)

    def setup(self):
        self.driver.get(self.url)
        time.sleep(2)  # Allow page to load fully

    def select_year_month(self, year, month):
        # Select year
        year_select = Select(self.driver.find_element(By.ID, "year"))
        year_select.select_by_value(year)
        time.sleep(1)

        # Select month
        month_select = Select(self.driver.find_element(By.ID, "month"))
        month_select.select_by_value(month)
        time.sleep(1)

    def has_next_page(self):
        try:
            next_button = self.driver.find_element(By.ID, "dataTable_next")
            return "disabled" not in next_button.get_attribute("class")
        except NoSuchElementException:
            return False

    def click_next_page(self):
        try:
            next_button = self.driver.find_element(By.ID, "dataTable_next")
            next_button.click()
            time.sleep(1)  # Wait for table to update
            return True
        except NoSuchElementException:
            return False

    def get_page_data(self, year):
        data = []
        # Wait for table to be visible
        table = self.wait.until(EC.presence_of_element_located((By.ID, "dataTable")))
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        # Skip header rows
        for row in rows[2:]:  # Skip both header rows
            cols = row.find_elements(By.TAG_NAME, "td")
            if cols:
                data.append({
                    'biller_operating_unit': cols[1].text,
                    'year': self.current_year,
                    'month': self.current_month,
                    'downtime_count': 0 if year != '2024-25' else cols[7].text,
                    'downtime_hhmm': cols[7].text if year != '2024-25' else cols[8].text,
                    'uptime_percentage': cols[8].text if year != '2024-25' else cols[9].text
                })
        return data

    def get_table_data(self, year):
        all_data = []
        page = 1
        
        while True:
            print(f"Processing page {page}")
            page_data = self.get_page_data(year)
            all_data.extend(page_data)
            
            if self.has_next_page():
                if not self.click_next_page():
                    break
                page += 1
            else:
                break

        print(f"Total records collected: {len(all_data)}")
        return all_data

    def scrape_all_periods(self, years=None, months=None):
        if years is None:
            years = ['2024-25', '2023-24', '2022-23', '2021-22']
        if months is None:
            months = ['December', 'November', 'October', 'September', 'August', 
                     'July', 'June', 'May', 'April']

        all_data = []
        
        for year in years:
            for month in months:
                try:
                    self.current_year = year
                    self.current_month = month
                    print(f"\nScraping data for {month} {year}")
                    
                    self.select_year_month(year, month)
                    data = self.get_table_data(year)
                    all_data.extend(data)
                    
                    # Wait between requests to avoid overwhelming the server
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Error scraping {month} {year}: {str(e)}")
                    continue

        return all_data

    def save_to_csv(self, data, filename="biller_operating_units_data.csv"):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def cleanup(self):
        self.driver.quit()

def main():
    scraper = BillerOperatingUnitScraper()
    try:
        scraper.setup()
        data = scraper.scrape_all_periods()
        scraper.save_to_csv(data)
    finally:
        scraper.cleanup()

if __name__ == "__main__":
    main()