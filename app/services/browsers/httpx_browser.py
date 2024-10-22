from httpx import Client

from app.services.browsers.basic_browser import BasicBrowser

__import__("urllib3").disable_warnings(
    __import__("urllib3").exceptions.InsecureRequestWarning
)
__import__("urllib3").disable_warnings()
__import__("urllib3").util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"


class HttpxBrowser(BasicBrowser):

    @classmethod
    def browser_connect(cls) -> Client:
        return Client()
