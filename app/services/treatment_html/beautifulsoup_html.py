from typing import AnyStr

from bs4 import BeautifulSoup

from app.services.treatment_html.html_basic import HtmlBasic


class BeautifulSoupHtml(HtmlBasic):

    @classmethod
    def html_connect(cls, html: AnyStr) -> BeautifulSoup:
        return BeautifulSoup(html, "lxml")
