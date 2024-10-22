from unittest.mock import patch

from app.services.browsers.httpx_browser import HttpxBrowser


@patch("app.services.browsers.httpx_browser.Client")
def test_httpx_browser(mock_session):
    mock_browser = HttpxBrowser.browser_connect()
    mock_session.assert_called_once()
    assert mock_browser == mock_session.return_value
