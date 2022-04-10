from webdriver_setup import WebDriverSetup
from page_object.pages.webfront_page import (
    LoginPage,
    HomePage,
    ViewPage,
    ExportPage
)
from tools import wait, get_config, get_credentials
from logger import logger


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
        login_page = LoginPage(
            self.driver,
            url=self.config['url'],
            username=self.credentials['username'],
            password=self.credentials['password']
        )
        login_page.zoom()
        login_page.login()

        # Home page
        home_page = HomePage(
            self.driver,
            download_path=self.config['download_path']
        )
        home_page.view_model_page()
        home_page.filter_data()

        # View page
        view_page = ViewPage(self.driver)
        view_page.open_collapsible_headers()
        view_page.tick_checkboxes()
        view_page.accept_changes()

        # Home page
        home_page.set_export_options()

        # Export page
        export_page = ExportPage(self.driver)
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


def main():
    webfront = WebFrontAutomation(
        config=get_config(),
        credentials=get_credentials()
    )
    webfront.run_driver()
    webfront.quit_driver()


if __name__ == '__main__':
    main()


# TODO: Maybe move the time delay calls here??
# TODO: Fix download path; make it more robust
