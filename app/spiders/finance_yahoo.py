from enum import Enum
from time import sleep
from typing import List, TypedDict

from dataclasses import dataclass
from selenium.common import (
    ElementClickInterceptedException, ElementNotInteractableException
)

from app.services.browsers.selenium_browser import SeleniumBrowser
from app.services.treatment_html.beautifulsoup_html import (
    BeautifulSoupHtml
)
from app.utils.logs import LogBots
from app.utils.robots import Robots


class FinanceYahooParamsRegions(Enum):
    ARG = "Argentina"
    AUS = "Australia"
    AUT = "Austria"
    BEL = "Belgium"
    BRA = "Brazil"
    CAN = "Canada"
    CHE = "Switzerland"
    CHL = "Chile"
    CHN = "China"
    DNK = "Denmark"
    EST = "Estonia"
    EGY = "Egypt"
    ESP = "Spain"
    FIN = "Finland"
    FRA = "France"
    GBR = "United Kingdom"
    GRC = "Greece"
    HKG = "Hong Kong SAR China"
    HUN = "Hungary"
    IDN = "Indonesia"
    IRL = "Ireland"
    ISR = "Israel"
    IND = "India"
    ISL = "Iceland"
    ITA = "Italy"
    JPN = "Japan"
    KOR = "South Korea"
    KWT = "Kuwait"
    LKA = "Sri Lanka"
    LTU = "Lithuania"
    LVA = "Latvia"
    MEX = "Mexico"
    MYS = "Malaysia"
    NLD = "Netherlands"
    NOR = "Norway"
    NZL = "New Zealand"
    PER = "Peru"
    PHL = "Philippines"
    PAK = "Pakistan"
    POL = "Poland"
    PRT = "Portugal"
    QAT = "Qatar"
    ROU = "Romania"
    RUS = "Russia"
    SAU = "Saudi Arabia"
    SWE = "Sweden"
    SGP = "Singapore"
    SUR = "Suriname"
    THA = "Thailand"
    TUR = "Turkey"
    TWN = "Taiwan"
    USA = "United States"
    VEN = "Venezuela"
    VNM = "Vietnam"
    ZAF = "South Africa"


class FinanceYahooResult(TypedDict):
    symbol: str
    name: str
    price: str


@dataclass
class FinanceYahooParams:
    regions: List[FinanceYahooParamsRegions]


class FinanceYahoo(SeleniumBrowser, BeautifulSoupHtml, Robots):
    def __init__(self, params: FinanceYahooParams):
        self.__logger = LogBots("Finance", "", "FinanceYahoo")
        self.__params = params
        self.__url = "https://finance.yahoo.com/screener/new"
        self.__browser = self.browser_connect(headless=False)
        self.__result = []

    @property
    def logger(self) -> LogBots:
        return self.__logger

    @property
    def params(self) -> FinanceYahooParams:
        return self.__params

    @property
    def url(self) -> str:
        return self.__url

    @property
    def browser(self):
        return self.__browser

    @property
    def result(self) -> List:
        return self.__result

    def _clean_filter(self) -> None:
        self.logger.info("RUN Clean filter")
        list_filter = ["Remove Sector",
                       "Remove Price (Intraday)",
                       "Remove Market Cap (Intraday)"]

        [
            self._selenium_find_timeout(
                self.browser,
                element=f'//button[@Title="{title}"]'
            ).click()
            for title in list_filter
        ]
        self._selenium_find_timeout(
            self.browser,
            element=f'//button[@title="Remove United States"]'
        ).click()
        self.logger.info("END Clean filter")

    def _select_region(self, region: FinanceYahooParamsRegions) -> None:
        self.logger.info(f"RUN Select Region: {region.name}")
        search_region = self._selenium_find_timeout(
            self.browser,
            element='//input[@placeholder="Find filters"]'
        )
        search_region.send_keys(region.value)
        xpath_region = (
            '//div[@id="dropdown-menu"]/div/div[2]/ul/li/label'
        )
        self._selenium_find_timeout(
            self.browser,
            element=xpath_region
        ).click()
        search_region.clear()

    def _select_regions(self) -> None:
        self.logger.info("Run Select Regions")
        self._selenium_find_timeout(
            self.browser,
            element='//*[@id="screener-criteria"]/div[2]/div[1]/div[1]'
                    '/div[1]/div/div[2]/ul/li/button'
        ).click()
        [self._select_region(region) for region in self.params.regions]
        self._selenium_find_timeout(
            self.browser,
            element='//div[@id="dropdown-menu"]/button[@title="Close"]'
        ).click()
        sleep(3)
        self._selenium_find_timeout(
            self.browser,
            element='//div[@data-test="button-content"]/button[1]'
        ).click()
        sleep(3)
        self.logger.info("END Select Regions")

    def _show_100_rows(self) -> None:
        self.logger.info("RUN Show 100 row")
        show_rows = self._selenium_find_timeout(
            self.browser,
            element='//span[@data-test="showRows-select-selected"]'
        )
        sleep(3)
        show_rows.click()
        sleep(3)
        show_rows.find_element(
            by=self._selenium_get_by('xpath'),
            value="//div[@data-value='100']"
        ).click()
        sleep(3)
        self.logger.info("END Show 100 row")

    def _click_next_page(self) -> None:
        element = self._selenium_find_timeout(
            self.browser,
            element='#scr-res-table > div.W\(100\%\).Mt\(15px\).'
                    'Ta\(end\) > button.Va\(m\).H\(20px\).'
                    'Bd\(0\).M\(0\).P\(0\).Fz\(s\).'
                    'Pstart\(10px\).O\(n\)\:f.Fw\(500\).'
                    'C\(\$linkColor\)',
            by=self._selenium_get_by('css'),
            ec=self._selenium_get_expected_conditions('presence')
        )
        try:
            element.click()
            element.send_keys(self._selenium_get_keys('home'))
        except (ElementClickInterceptedException,
                ElementNotInteractableException):
            pass
        sleep(8)

    def _add_values_result(self, num_page: int = 1) -> None:
        self.logger.info(f"RUN Page: {num_page}")
        page = self.html_connect(self.browser.page_source)
        for tr in page.select(
                "#scr-res-table > div.Ovx\(a\).Ovx\(h\)--print.Ovy\(h\)."
                "W\(100\%\) > table > tbody > tr"
        ):
            td = tr.find_all('td')
            self.result.append(
                FinanceYahooResult(
                    symbol=td[0].text,
                    name=td[1].text,
                    price=td[2].text
                )
            )

        next_page = self.browser.find_element(
            self._selenium_get_by('xpath'),
            '//*[@id="scr-res-table"]/div[2]/button[3]'
        ).get_attribute('aria-disabled')
        if next_page and next_page == "false":
            self._click_next_page()
            return self._add_values_result(num_page + 1)
        self.logger.info(f"END result: {len(self.result)}")

    def _save_csv(self) -> str:
        self.logger.info("RUN Save CSV")
        result = self.save_csv(
            self.result,
            crawler_name="finance_yahoo"
        ) if self.result else None
        self.logger.info(f"END Save CSV: {result}")
        return result

    def run(self) -> str:
        try:
            self.logger.info(f"RUN Crawler -->")
            self.browser.get(self.url)
            self._clean_filter()
            self._select_regions()
            self._show_100_rows()
            self._add_values_result()
            result = self._save_csv()
            self.logger.info(f"END Crawler <--")
            return result

        finally:
            self.browser.close()


if __name__ == '__main__':
    print(f"Available Options: "
          f"{[x.value for x in FinanceYahooParamsRegions]}")
    value_input = str(input("Regions: ")).split(',')
    try:
        values = [FinanceYahooParamsRegions(x) for x in value_input]
        FinanceYahoo(
            params=FinanceYahooParams(
                regions=values)
        ).run()
    except ValueError:
        print(f"{value_input} not found")


