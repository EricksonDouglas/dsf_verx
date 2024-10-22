from unittest.mock import patch, MagicMock

from app.services.browsers.selenium_browser import (
    SeleniumBrowser, TimeoutException
)


@patch.object(SeleniumBrowser, "_get_selenium_binary_webdriver")
@patch.object(SeleniumBrowser, "_selenium_options")
@patch("app.services.browsers.selenium_browser.Service")
@patch("app.services.browsers.selenium_browser.DesiredCapabilities")
@patch("app.services.browsers.selenium_browser.Chrome")
def test_selenium_browser_browser_connect(
        mock_chrome,
        _mock_d_c,
        mock_service,
        mock_selenium_options,
        mock_get_binary_webdriver
):
    mock_instance = SeleniumBrowser.browser_connect()
    assert mock_selenium_options.called
    assert mock_service.called
    assert mock_chrome.called
    assert mock_get_binary_webdriver.called
    assert mock_instance == mock_chrome.return_value


@patch("app.services.browsers.selenium_browser.mkdtemp")
@patch.object(SeleniumBrowser, "_get_selenium_download_folder_path")
@patch.object(SeleniumBrowser, "_get_selenium_binary_browser")
@patch("app.services.browsers.selenium_browser.ChromeOptions")
def test_selenium_browser_selenium_options(
        mock_chrome_options,
        mock_get_binary_browser,
        mock_get_selenium_download_folder_path,
        _mock_mkdtemp
):
    mock_instance = SeleniumBrowser._selenium_options(
        headless=True,
        disable_images=True,
        extra_options=False,
        custom_dir=False,
        page_load_strategy='normal'
    )
    assert mock_get_binary_browser.called
    assert mock_get_selenium_download_folder_path.called
    assert mock_chrome_options.called
    assert mock_instance.page_load_strategy == 'normal'


@patch("app.services.browsers.selenium_browser.WebDriverWait")
def test_selenium_browser_selenium_find_timeout(
        mock_web_driver_wait
):
    mock_driver = MagicMock()
    mock_element = "xxx"
    mock_instance = SeleniumBrowser._selenium_find_timeout(
        mock_driver,
        element=mock_element
    )
    assert mock_web_driver_wait.called
    assert (mock_instance ==
            mock_web_driver_wait.return_value.until.
            return_value)


@patch("app.services.browsers.selenium_browser.WebDriverWait")
def test_selenium_browser_selenium_find_timeout_error(
        mock_web_driver_wait
):
    mock_web_driver_wait.return_value.until.side_effect = TimeoutException()
    mock_driver = MagicMock()
    mock_element = "xxx"

    mock_instance = SeleniumBrowser._selenium_find_timeout(
        mock_driver,
        element=mock_element
    )
    assert mock_instance is None


@patch("app.services.browsers.selenium_browser.By")
def test_selenium_browser_selenium_get_by(mock_by):
    mock_instance_xpath = SeleniumBrowser._selenium_get_by(
        "xpath"
    )
    assert mock_instance_xpath == mock_by.XPATH
    mock_instance_css = SeleniumBrowser._selenium_get_by(
        "css"
    )
    assert (mock_instance_css ==
            mock_by.CSS_SELECTOR)


@patch("app.services.browsers.selenium_browser.e_c")
def test_selenium_browser_selenium_get_expected_conditions(mock_ec):
    mock_presence = SeleniumBrowser._selenium_get_expected_conditions(
        "presence"
    )
    assert (mock_presence ==
            mock_ec.presence_of_element_located)
    mock_visibility = SeleniumBrowser._selenium_get_expected_conditions(
        "visibility"
    )
    assert (mock_visibility ==
            mock_ec.visibility_of_element_located)


@patch("app.services.browsers.selenium_browser.Keys")
def test_selenium_browser_selenium_get_key(mock_key):
    mock_home = SeleniumBrowser._selenium_get_keys(
        "home"
    )
    assert (mock_home ==
            mock_key.CONTROL.__add__.return_value)


def test_selenium_browser_get_environment():
    mock_env_binary_browser = SeleniumBrowser._get_selenium_binary_browser()
    mock_env_binary_webdriver = SeleniumBrowser._get_selenium_binary_browser()
    mock_env_download_folder_path = SeleniumBrowser._get_selenium_download_folder_path()
    assert isinstance(mock_env_binary_browser, str)
    assert isinstance(mock_env_binary_webdriver, str)
    assert isinstance(mock_env_download_folder_path, str)
