import os
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException
)

from page_object.locators import (
    WebFrontLoginPageLocators,
    WebFrontHomePageLocators,
    WebFrontViewPageLocators,
    WebFrontExportPageLocators
)
from page_object.pages.base_page import BasePage
from tools import wait
from logger import logger


class WebFrontLoginPage(BasePage):

    def __init__(self, driver, url: str, username: str, password: str) -> None:
        super().__init__(driver)

        self.url = url
        self.username = username
        self.password = password

        self.driver.get(self.url)
        wait(low=5)

    def zoom(self) -> None:
        logger.info('Setting zoom level to 100%')
        self.driver.execute_script(WebFrontLoginPageLocators.zoom_script)
        wait(low=2)

    def login(self) -> None:
        logger.info('Entering username')
        self.enter_text(WebFrontLoginPageLocators.username_field, self.username)
        wait(low=1)

        logger.info('Entering password')
        self.enter_text(WebFrontLoginPageLocators.password_field, self.password)
        wait(low=1)

        logger.info('Clicking login button')
        self.click(WebFrontLoginPageLocators.login_button)
        wait(low=5, high=10)


class WebFrontHomePage(BasePage):

    def __init__(self, driver, download_path: Path) -> None:
        super().__init__(driver)
        self.download_path = download_path

    def view_model_page(self) -> None:
        logger.info('Clicking model page button')
        self.click(WebFrontHomePageLocators.model_page_button)
        wait(low=5, high=8)

    def filter_data(self) -> None:
        logger.info('Filtering data')
        self.check_presence(WebFrontHomePageLocators.more_results_element)
        self.click(WebFrontHomePageLocators.view_button)
        wait(low=5)

    def set_export_options(self) -> None:
        logger.info('Setting export options')
        self.check_presence(WebFrontHomePageLocators.export_options)
        self.click(WebFrontHomePageLocators.export_options)
        wait(low=2)

    def wait_download(self) -> None:
        logger.info('Waiting for file to be downloaded')

        while True:
            logger.info('Checking if data is downloaded')
            wait(low=1)

            files = [file for file in os.listdir(self.download_path) if file != '.DS_Store']

            if len(files) == 1 and files[0].endswith('.csv'):
                break


class WebFrontViewPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def open_collapsible_headers(self) -> None:
        # TODO: Add range in parameters
        logger.info('Opening collapsible headers')

        for i in range(1, 16):
            # header_xpath = f'//*[@id="column_table"]/div[{i}]'
            header_xpath = f'/html/body/div[8]/div[6]/div/div[2]/div/ul/li[2]/div/div[{i}]'
            select = self.driver.find_element(By.XPATH, header_xpath)

            self.driver.execute_script(
                'arguments[0].setAttribute("class", "collapsible-section-container")',
                select
            )

            wait(high=2)

    def tick_checkboxes(self) -> None:
        td_drivers = self.driver.find_elements(*WebFrontViewPageLocators.td_class)

        for td_index, td_driver in enumerate(td_drivers, start=1):
            wait(high=2)

            td_text = td_driver.find_element(*WebFrontViewPageLocators.checkbox_label).text
            logger.info(f'Clicking checkbox: {td_text}')

            checkbox_element = './input[@type="checkbox"]'
            # checkbox_driver = td_driver.find_element(*WebFrontViewPageLocators.checkbox_element)
            checkbox_driver = td_driver.find_element(By.XPATH, checkbox_element)

            try:
                self.check_presence(
                    WebFrontViewPageLocators.checkbox_element,
                    td_driver
                )

                if not checkbox_driver.is_selected():
                    try:
                        self.click(
                            WebFrontViewPageLocators.checkbox_element,
                            td_driver
                        )

                    except TimeoutException:
                        self.click(
                            WebFrontViewPageLocators.checkbox_element,
                            td_driver
                        )

                    except ElementClickInterceptedException:
                        checkbox_driver.send_keys(WebFrontViewPageLocators.page_down)
                        wait(high=2)

                        self.click(
                            WebFrontViewPageLocators.checkbox_element,
                            td_driver
                        )

            except TimeoutException:
                self.check_presence(
                    WebFrontViewPageLocators.checkbox_element,
                    td_driver
                )

        wait(low=1)

    def accept_changes(self) -> None:
        logger.info('Accepting changes')
        self.click(WebFrontViewPageLocators.accept_changes_button)
        wait(low=5)


class WebFrontExportPage(BasePage):

    def __init__(self, driver) -> None:
        super().__init__(driver)

    def choose_filetype(self) -> None:
        logger.info('Selecting filetype')
        self.select_value(WebFrontExportPageLocators.export_filetype, 'csv')
        wait(low=1)

    def choose_export_all(self) -> None:
        logger.info('Selecting export all option')
        self.click(WebFrontExportPageLocators.export_all_element)
        wait(low=1)

    def download_data(self) -> None:
        logger.info('Downloading data')
        self.click(WebFrontExportPageLocators.export_button)
        wait(low=10)
