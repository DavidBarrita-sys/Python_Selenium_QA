from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# Base page class
class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, locator):
        return self.driver.find_element(by, locator)

    def find_elements(self, by, locator):
        return self.driver.find_elements(by, locator)

    def click(self, by, locator):
        self.find_element(by, locator).click()

    def select_by_visible_text(self, by, locator, text):
        Select(self.find_element(by, locator)).select_by_visible_text(text)

    def set_year(self, input_id, year):
        try:
            year_input = self.find_element(By.ID, input_id)
            year_input.clear()
            year_input.send_keys(str(year))
            print(f"Set year to: {year}")
        except NoSuchElementException:
            print(f"Input field with ID '{input_id}' not found.")