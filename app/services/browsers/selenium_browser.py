from tempfile import mkdtemp
from typing import Literal, Optional

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import (
    DesiredCapabilities
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.support.ui import WebDriverWait

from app.services.browsers.basic_browser import BasicBrowser


class SeleniumBrowser(BasicBrowser):

    @staticmethod
    def _get_selenium_binary_browser() -> str:
        return 'layers/chrome-linux/chrome'

    @staticmethod
    def _get_selenium_binary_webdriver() -> str:
        return "layers/chromedriver"

    @staticmethod
    def _get_selenium_download_folder_path() -> str:
        """Method used to get the selenium download folder path"""
        return "/tmp"

    @classmethod
    def browser_connect(
            cls,
            headless: bool = True,
            disable_images: bool = True,
            log_pref_save: bool = True,
            page_load_strategy: Literal[
                'normal', 'eager', 'none'] = "normal",
            extra_options: bool = False,
            custom_dir: bool = False
    ) -> Chrome:
        """
        Method used to instantiate a selenium webdriver with the chromedriver library using different parameters

        Param defaults:
        - headless = True -> used to run the browser in headless mode (similar to phantomJS)
        - disable_images = True -> used to disable the loading of images in the browser
        - log_pref_save = True -> used to save the browser logs
        - use_selenium_wire = False -> used to use the selenium wire library
        - undetected_chromedriver = False -> used to use the undetected chromedriver library
        - page_load_strategy = "normal" -> used to set the page load strategy. Options are "normal", "eager" and "none".
        - user_agent_override = False -> used to force user-agent to an old version
        """

        caps = DesiredCapabilities.CHROME

        if log_pref_save:
            caps["goog:loggingPrefs"] = {"performance": "ALL"}

        options = cls._selenium_options(
            headless=headless,
            disable_images=disable_images,
            page_load_strategy=page_load_strategy,
            extra_options=extra_options,
            custom_dir=custom_dir
        )

        return Chrome(
            options=options,
            desired_capabilities=caps or None,
            service=Service(
                executable_path=cls._get_selenium_binary_webdriver()
            ),
            service_log_path="/tmp/geckodriver.log",
        )

    @classmethod
    def _selenium_options(
            cls,
            headless,
            disable_images,
            page_load_strategy,
            extra_options,
            custom_dir,
    ) -> ChromeOptions:
        """Method used to instantiate a selenium webdriver options"""

        options = ChromeOptions()

        options.binary_location = cls._get_selenium_binary_browser()

        if headless:
            options.add_argument("--headless")

        if disable_images:
            options.add_argument("--blink-settings=imagesEnabled=false")
            options.add_argument("--load-images=no")
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": cls._get_selenium_download_folder_path(),
                "download.prompt_for_download": False,
                "profile.default_content_settings.popups": 0,
                "safebrowsing.enabled": False,
                "directory_upgrade": True,
            },
        )
        options.add_argument("--no-proxy-server")
        options.add_argument('--proxy-server="direct://"')
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--single-process")
        options.add_argument("--no-zygote")
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/109.0.5414.74 Safari/537.36"
        )

        options.add_argument("--disable-dev-tools")

        if extra_options:
            # !! Possiveis erros de execução no Lambda
            options.add_argument("--disable-breakpad")
            options.add_argument("--incognito")
            options.add_argument("--disable-extensions")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--disable-setuid-sandbox")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            options.add_argument(
                "--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-background-networking")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--ignore-ssl-errors=true")
            options.add_argument("--disable-popup-blocking")

        if custom_dir:
            # !! Possiveis limitações de armazenamento no Lambda

            options.add_argument(f"--user-data-dir={mkdtemp()}")
            options.add_argument(f"--data-path={mkdtemp()}")
            options.add_argument(f"--disk-cache-dir={mkdtemp()}")

        options.set_capability("unhandledPromptBehavior", "accept")
        options.page_load_strategy = page_load_strategy

        return options



    @staticmethod
    def _selenium_find_timeout(
            driver: WebDriver,
            *,
            time: int = 60,
            by: By = By.XPATH,
            element: str,
            ec: e_c = e_c.visibility_of_element_located,
    ) -> Optional[WebElement]:

        try:
            element = (by, element)
            return WebDriverWait(driver, time).until(ec(element))
        except TimeoutException:
            return None

    @staticmethod
    def _selenium_get_by(by: Literal['xpath', 'css']) -> By:
        map_by = {
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR
        }
        return map_by[by]

    @staticmethod
    def _selenium_get_expected_conditions(
            ec: Literal['presence', 'visibility']
    ) -> e_c:
        map_ec = {
            'presence': e_c.presence_of_element_located,
            'visibility': e_c.visibility_of_element_located
        }
        return map_ec[ec]

    @staticmethod
    def _selenium_get_keys(key: Literal['home']) -> Keys:
        map_keys = {
            'home': Keys.CONTROL + Keys.HOME
        }
        return map_keys[key]
