import os
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException
)

from page_object.locators import (
    RetailDeckLoginPageLocators,
    RetailDeckHomePageLocators,
    RetailDeckViewPageLocators,
    RetailDeckExportPageLocators
)
from page_object.pages.base_page import BasePage
from tools import wait
from logger import logger


class RetailDeckLoginPage(BasePage):

    def __init__(self, driver, url: str, username: str, password: str) -> None:
        super().__init__(driver)

        self.url = url
        self.username = username
        self.password = password

        self.driver.get(self.url)
        wait(low=5)

    def zoom(self) -> None:
        logger.info('Setting zoom level to 100%')
        self.driver.execute_script(RetailDeckLoginPageLocators.zoom_script)
        wait(low=2)

    def login(self) -> None:
        logger.info('Entering username')
        self.enter_text(RetailDeckLoginPageLocators.username_field, self.username)
        wait(low=1)

        logger.info('Entering password')
        self.enter_text(RetailDeckLoginPageLocators.password_field, self.password)
        wait(low=1)

        logger.info('Clicking login button')
        self.click(RetailDeckLoginPageLocators.login_button)
        wait(low=5, high=10)


class RetailDeckHomePage(BasePage):

    def __init__(self, driver, download_path: Path) -> None:
        super().__init__(driver)
        self.download_path = download_path

    def set_view_options(self) -> None:
        logger.info('Clicking view options')
        self.check_presence(RetailDeckHomePageLocators.more_results_element)
        self.click(RetailDeckHomePageLocators.view_options_button)
        wait(low=5)

    def set_export_options(self) -> None:
        logger.info('Setting export options')
        self.check_presence(RetailDeckHomePageLocators.export_options)
        self.click(RetailDeckHomePageLocators.export_options)
        wait(low=2)

    def wait_download(self) -> None:
        logger.info('Waiting for file to be downloaded')

        while True:
            logger.info('Checking if data is downloaded')
            wait(low=1)

            files = [file for file in os.listdir(self.download_path) if file != '.DS_Store']

            if len(files) == 1 and files[0].endswith('.csv'):
                break


class RetailDeckViewPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def open_collapsible_headers(self) -> None:
        logger.info('Opening collapsible headers')

        for i in range(1, 10):
            header_xpath = f"/html/body/div[8]/div[4]/div/div[2]/form/ul/li[2]/div/div[{i}]"
            select = self.driver.find_element(By.XPATH, header_xpath)

            self.driver.execute_script(
                'arguments[0].setAttribute("class", "collapsible-section-container")',
                select,
            )

            wait(high=2)

    def tick_checkboxes(self) -> None:
        td_drivers = self.driver.find_elements(*RetailDeckViewPageLocators.td_class)

        for td_index, td_driver in enumerate(td_drivers, start=1):
            wait(high=2)

            td_text = td_driver.find_element(*RetailDeckViewPageLocators.checkbox_label).text
            logger.info(f'Clicking checkbox: {td_text}')

            checkbox_element = './input[@type="checkbox"]'
            checkbox_driver = td_driver.find_element(By.XPATH, checkbox_element)

            try:
                self.check_presence(
                    RetailDeckViewPageLocators.checkbox_element,
                    td_driver
                )

                if not checkbox_driver.is_selected():
                    try:
                        self.click(
                            RetailDeckViewPageLocators.checkbox_element,
                            td_driver
                        )

                    except TimeoutException:
                        self.click(
                            RetailDeckViewPageLocators.checkbox_element,
                            td_driver
                        )

                    except ElementClickInterceptedException:
                        checkbox_driver.send_keys(RetailDeckViewPageLocators.page_down)
                        wait(high=2)

                        self.click(
                            RetailDeckViewPageLocators.checkbox_element,
                            td_driver
                        )

            except TimeoutException:
                self.check_presence(
                    RetailDeckViewPageLocators.checkbox_element,
                    td_driver
                )

        wait(low=1)

    def accept_changes(self) -> None:
        logger.info('Accepting changes')
        self.click(RetailDeckViewPageLocators.accept_changes_button)
        wait(low=5)


class RetailDeckExportPage(BasePage):

    def __init__(self, driver) -> None:
        super().__init__(driver)

    def choose_filetype(self) -> None:
        logger.info('Selecting filetype')
        self.select_value(RetailDeckExportPageLocators.export_filetype, 'csv')
        wait(low=1)

    def choose_export_all(self) -> None:
        logger.info('Selecting export all option')
        self.click(RetailDeckExportPageLocators.export_all_element)
        wait(low=1)

    def download_data(self) -> None:
        logger.info('Downloading data')
        self.click(RetailDeckExportPageLocators.export_button)
        wait(low=10)
