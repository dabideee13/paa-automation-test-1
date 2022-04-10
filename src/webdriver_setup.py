from pathlib import Path

from selenium import webdriver

from tools import wait


class WebDriverSetup:

    def __init__(
        self,
        download_path: Path,
        headless: bool = False
    ) -> None:
        self.download_path = str(download_path)
        self.headless = headless

    def set_driver(self) -> None:
        options = webdriver.FirefoxOptions()
        options.headless = self.headless

        options.set_preference('browser.download.folderList', 2)
        options.set_preference('browser.download.manager.showWhenStarting', False)
        options.set_preference('browser.download.dir', self.download_path)

        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(30)
        driver.maximize_window()
        wait(low=2)

        return driver
