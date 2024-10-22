from unittest.mock import patch

from app.services.treatment_html.lxml_html import (
    LxmlHtml
)


@patch("app.services.treatment_html.lxml_html.fromstring")
def test_beautiful_soup_browser(mock_lxml):
    mock_html = ""
    mock_instance = LxmlHtml.html_connect(mock_html)
    mock_lxml.assert_called_once_with(mock_html)
    assert mock_instance == mock_lxml.return_value
