from pathlib import Path

from page_object.locators import (
    PortalLoginPageLocators,
    PortalHomePageLocators,
    PortalSalesOrdersPageLocators,
    PortalDealerOrderStatusPageLocators
)
from page_object.base_page import BasePage
from tools import wait
from logger import logger


class PortalLoginPage(BasePage):

    def __init__(self, driver, url: str, username: str, password: str) -> None:
        super().__init__(driver)

        self.url = url
        self.username = username
        self.password = password

        self.driver.get(self.url)
        wait(low=5)

    def zoom(self) -> None:
        logger.info('Setting zoom level to 100%')
        self.driver.execute_script(PortalLoginPageLocators.zoom_script)
        wait(low=2)

    def login(self) -> None:
        logger.info('Entering username')
        self.enter_text(PortalLoginPageLocators.username_field, self.username)
        wait(low=1)

        logger.info('Entering password')
        self.enter_text(PortalLoginPageLocators.password_field, self.password)
        wait(low=1)

        logger.info('Clicking login button')
        self.click(PortalLoginPageLocators.login_button)
        wait(low=5, high=10)


class PortalHomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def click_sales_orders(self):
        logger.info('Opening `Sales Orders`')
        self.click(PortalHomePageLocators.sales_orders)
        wait(low=5)


class PortalSalesOrdersPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def click_dealer_order_status(self):
        logger.info('Opening `Dealer Order Status`')
        self.click(PortalSalesOrdersPageLocators.dealer_order_status)
        wait(low=5)


class PortalDealerOrderStatusPage(BasePage):

    def __init__(self, driver, download_path: Path):
        super().__init__(driver)
        self.download_path = download_path

    def set_export_options(self):
        logger.info('Setting export options')
        self.click(PortalDealerOrderStatusPageLocators.export_options)
        wait(low=2)

    def download_data(self):
        logger.info('Downloading data')
        self.click(PortalDealerOrderStatusPageLocators.export_button)
        wait(low=2)

    def wait_download(self) -> None:
        logger.info('Waiting for file to be downloaded')

        while True:
            logger.info('Checking if data is downloaded')
            wait(low=1)

            files = [file for file in os.listdir(self.download_path) if file != '.DS_Store']

            if len(files) == 1 and files[0].endswith('.csv'):
