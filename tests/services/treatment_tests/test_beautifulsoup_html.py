from unittest.mock import patch

from app.services.treatment_html.beautifulsoup_html import (
    BeautifulSoupHtml
)


@patch("app.services.treatment_html.beautifulsoup_html.BeautifulSoup")
def test_beautiful_soup_browser(mock_beautiful_soup):
    mock_html = ""
    mock_instance = BeautifulSoupHtml.html_connect(mock_html)
    mock_beautiful_soup.assert_called_once_with(mock_html, 'lxml')
    assert mock_instance == mock_beautiful_soup.return_value
