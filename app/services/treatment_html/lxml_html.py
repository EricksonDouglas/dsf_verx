from typing import AnyStr

from lxml.html import fromstring, HtmlElement

from app.services.treatment_html.html_basic import HtmlBasic


class LxmlHtml(HtmlBasic):

    @classmethod
    def html_connect(cls, html: AnyStr) -> HtmlElement:
        return fromstring(
            html.decode("UTF-8") if isinstance(html, bytes) else html
        )
