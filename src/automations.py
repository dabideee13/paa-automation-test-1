from webdriver_setup import WebDriverSetup
from page_object.pages.webfront_page import (
    WebFrontLoginPage,
    WebFrontHomePage,
    WebFrontViewPage,
    WebFrontExportPage
)
from page_object.pages.retail_deck_page import (
    RetailDeckLoginPage,
    RetailDeckHomePage,
    RetailDeckViewPage,
    RetailDeckExportPage
)
from logger import logger
from tools import wait


class WebFrontAutomation:

    def __init__(self, config: dict[str, str], credentials: dict[str, str]) -> None:
        self.config = config
        self.credentials = credentials

        self.driver = self._setup_driver()

    def _setup_driver(self):
        setup = WebDriverSetup(
            download_path=self.config['download_path'],
            headless=self.config['headless']
        )
        return setup.set_driver()

    def run_driver(self) -> None:
        # Login page
        login_page = WebFrontLoginPage(
            self.driver,
            url=self.config['url'],
            username=self.credentials['username'],
            password=self.credentials['password']
        )
        login_page.zoom()
        login_page.login()

        # Home page
        home_page = WebFrontHomePage(
            self.driver,
            download_path=self.config['download_path']
        )
        home_page.view_model_page()
        home_page.filter_data()

        # View page
        view_page = WebFrontViewPage(self.driver)
        view_page.open_collapsible_headers()
        view_page.tick_checkboxes()
        view_page.accept_changes()

        # Home page
        home_page.set_export_options()

        # Export page
        export_page = WebFrontExportPage(self.driver)
        export_page.choose_filetype()
        export_page.choose_export_all()
        export_page.download_data()

        # Home page
        home_page.wait_download()

    def quit_driver(self) -> None:
        if self.driver is not None:
            logger.info('Closing driver')
            wait(low=3)

            self.driver.close()
            self.driver.quit()


class RetailDeckAutomation:

    def __init__(self, config: dict[str, str], credentials: dict[str, str]) -> None:
        self.config = config
        self.credentials = credentials

        self.driver = self._setup_driver()

    def _setup_driver(self):
        setup = WebDriverSetup(
            download_path=self.config['download_path'],
            headless=self.config['headless']
        )
        return setup.set_driver()

    def run_driver(self) -> None:
        # Login page
        login_page = RetailDeckLoginPage(
            self.driver,
            url=self.config['url'],
            username=self.credentials['username'],
            password=self.credentials['password']
        )
        login_page.zoom()
        login_page.login()

        # Home page
        home_page = RetailDeckHomePage(
            self.driver,
            download_path=self.config['download_path']
        )
        home_page.set_view_options()

        # View page
        view_page = RetailDeckViewPage(self.driver)
        view_page.open_collapsible_headers()
        view_page.tick_checkboxes()
        view_page.accept_changes()

        # Home page
        home_page.set_export_options()

        # Export page
        export_page = RetailDeckExportPage(self.driver)
        export_page.choose_filetype()
        export_page.choose_export_all()
        export_page.download_data()

        # Home page
        home_page.wait_download()

    def quit_driver(self) -> None:
        if self.driver is not None:
            logger.info('Closing driver')
            wait(low=3)

            self.driver.close()
            self.driver.quit()


# TODO: Maybe move the time delay calls here??
# TODO: Fix download path; make it more robust
# TODO: Wrap this (to not repeat the codes)
# TODO: Add pipeline class to just input the steps without having to rewrite everything
