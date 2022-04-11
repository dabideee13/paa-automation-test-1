from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class RetailDeckLoginPageLocators:
    zoom_script = 'document.body.style.zoom="100%"'
    username_field = (By.XPATH, '//*[@id="login_box_username"]')
    password_field = (By.XPATH, '//*[@id="login_box_password"]')
    # login_button = (By.XPATH, '//*[@id="login-button"]')
    login_button = (By.ID, 'login-button')


class RetailDeckHomePageLocators:
    view_options_button = (By.XPATH, '//*[@id="show_hide_columns_btn"]')
    more_results_element = (By.XPATH, '//*[@id="ajax_data_table"]/tbody/tr[201]/td')
    export_options = "/html/body/div[8]/div[3]/div[3]/p[4]"


class RetailDeckViewPageLocators:
    td_class = (By.XPATH, '//td[@class="cb"]')
    checkbox_label = (By.XPATH, "./following-sibling::td")
    checkbox_element = (By.XPATH, './input[@type="checkbox"]')
    page_down = Keys.PAGE_DOWN
    accept_changes_button = (By.XPATH, '//*[@id="modify_view"]/ul/li[3]/div/button[1]')


class RetailDeckExportPageLocators:
    export_all_element = (By.ID, "num_results_to_export_all")
    export_button = (By.XPATH, '//*[@id="modify_view"]/ul/li[6]/div/button[1]')
    export_filetype = (By.ID, 'file_format')


class WebFrontLoginPageLocators:
    zoom_script = 'document.body.style.zoom="100%"'
    username_field = (By.ID, 'login_box_username')
    password_field = (By.ID, 'login_box_password')
    login_button = (By.XPATH, '//*[@id="login_form"]/ul/li[6]/button')


class WebFrontHomePageLocators:
    model_page_button = (By.XPATH, '//*[@id="dashboard-menu"]/div/div[1]/div[1]/div[1]/ul/li[1]/a')
    export_options = (By.XPATH, '/html/body/div[8]/div[3]/div[4]/p[4]')
    more_results_element = (By.XPATH, '//*[@id="ajax_data_table"]/tbody/tr[251]/td')
    view_button = (By.ID, 'show_hide_columns_btn')


class WebFrontViewPageLocators:
    collapsible_class = 'arguments[0].setAttribute("class", "collapsible-section-container")'
    td_class = (By.XPATH, '//td[@class="cb"]')
    checkbox_element = (By.XPATH, './input[@type="checkbox"]')
    accept_changes_button = (By.XPATH, '//*[@id="modify_view"]/ul/li[3]/div/button[1]')
    checkbox_label = (By.XPATH, './following-sibling::td')
    page_down = Keys.PAGE_DOWN


class WebFrontExportPageLocators:
    export_all_element = (By.ID, 'num_results_to_export_all')
    export_filetype = (By.ID, 'file_format')
    export_button = (By.XPATH, '//*[@id="modify_view"]/ul/li[6]/div/button[1]')


class PortalLoginPageLocators:
    pass


class PortalHomePageLocators:
    pass
