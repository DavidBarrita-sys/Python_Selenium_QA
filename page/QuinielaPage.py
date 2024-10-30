from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from page.BasePage import BasePage


class QuinielaPage(BasePage):
    URL = "https://mean-machine-qa.vercel.app/"

    def open(self):
        self.driver.get(self.URL)
        print("Page Title:", self.driver.title)

    def click_fill_quiniela(self):
        self.click(By.LINK_TEXT, "Llenar Quiniela")

    def get_team_names(self):
        team_elements = self.find_elements(By.CLASS_NAME, "teamName")
        return [team.text for team in team_elements]

    def click_tied_game_options(self, count=5):
        empate_buttons = self.find_elements(By.CLASS_NAME, "tiedGame")
        for i, button in enumerate(empate_buttons):
            if i >= count:
                break
            button.click()
            print("Clicked an 'Empate' option.")

    def select_user(self, user_name):
        try:
            self.select_by_visible_text(By.ID, "user", user_name)
            print(f"Selected user: {user_name}")
        except NoSuchElementException:
            print(f"User '{user_name}' not found in the dropdown.")

    def select_specific_year(self, year):
        self.set_year("year", year)

    def click_save_forecast(self):
        self.click(By.ID, "saveForecast")

    def verify_text_present(self, text):
        try:
            element = self.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
            print(f"Text '{text}' is present on the page.")
            return True
        except NoSuchElementException:
            print(f"Text '{text}' is not present on the page.")
            return False

    def confirm_save(self):
        try:
            save_button = self.find_element(By.XPATH, "//*[contains(text(), 'Sí, guardar')]")
            save_button.click()
            print("Clicked 'Sí, guardar' button.")
        except NoSuchElementException:
            print("'Sí, guardar' button not found.")

    def close_popup(self):
        try:
            ok_button = self.find_element(By.CLASS_NAME, "swal2-confirm")
            ok_button.click()
        except NoSuchElementException:
            print("OK button not found; popup may not be present.")

    def get_team_elements(self):
        return self.find_elements(By.CLASS_NAME, "teamName")

    def click_team_names(self):
        team_elements = self.get_team_elements()
        assert len(team_elements) > 0, "No team elements found on the page."

        for team in team_elements:
            team.click()

    def click_my_score(self):
        self.click(By.XPATH,"//nav//a[span[text()='Llenar Quiniela']]")

    def get_puntaje_total(self):
        try:
            puntaje_text = self.find_element(By.XPATH, "//div[@id='tableContainer']//caption/span").text
            label, value = puntaje_text.split(": ")
            return label, int(value)
        except NoSuchElementException:
            print("'Puntaje Total' element not found.")
            return None, None

    def count_success_elements(self):
        success_elements = self.find_elements(By.CLASS_NAME, "success")
        count = len(success_elements)
        print(f"Number of elements with class 'success': {count}")
        return count