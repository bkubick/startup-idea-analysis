# coding: utf-8

from __future__ import annotations

from enum import Enum
import time
import typing

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .. import models


class CompanySize(Enum):
    ONE_TO_TEN = '1-10-employees'
    ELEVEN_TO_FIFTY = '11-50-employees'
    FIFTY_ONE_TO_TWO_HUNDRED = '51-200-employees'


class Location(Enum):
    FULLY_REMOTE = 'fully-remote'
    CHICAGO = 'chicago'
    COLORADO = 'colorado'
    PEORIA = 'peoria'
    PHOENIX = 'phoenix-mesa-scottsdale'


class BuiltInScraper:
    """ Scrapes companies from builtin.com.

        Private Attributes:
            _companies_base_url (str): The base url to fetch companies from.
    """
    _companies_base_url: str = 'https://builtin.com/companies'

    def _generate_companies_url(self, sizes: typing.Optional[typing.List[CompanySize]] = None,
                                locations: typing.Optional[typing.List[Location]] = None,
                                page: int = 1) -> str:
        """ Generates the url to fetch companies from.

            Args:
                sizes (typing.Optional[typing.List[CompanySize]]): The sizes of the companies to fetch.
                locations (typing.Optional[typing.List[Location]]): The locations of the companies to fetch.
                page (int): The page of results to fetch.
            
            Returns:
                str: The url to fetch companies
        """
        url = self._companies_base_url

        if locations:
            url += '/location'

            for location in locations:
                url += f'/{location.value}'
        
        if sizes:
            url += '/size'

            for size in sizes:
                url += f'/{size.value}'

        return f'{url}?page={page}'

    def _extract_company_name(self, company_card: BeautifulSoup) -> str:
        """ Extracts the name of the company from the company card.

            Args:
                company_card (BeautifulSoup): The company card to extract the name from.
            
            Returns:
                str: The name of the company.
        """
        company_name = company_card.find('h2', class_='company-name')
        name = company_name.find('a').text
        return name.strip()

    def _extract_company_industries(self, company_card: BeautifulSoup) -> typing.List[str]:
        """ Extracts the industries of the company from the company card.

            Args:
                company_card (BeautifulSoup): The company card to extract the industries from.
            
            Returns:
                typing.List[str]: The industries of the company.
        """
        industry_section: BeautifulSoup = company_card.find('h4', class_='company-industries')
        industries: typing.List[BeautifulSoup] = industry_section.find_all('li')
        return [industry.text.strip() for industry in industries]

    def _extract_company_description(self, company_card: BeautifulSoup) -> str:
        """ Extracts the description of the company from the company card.

            Args:
                company_card (BeautifulSoup): The company card to extract the description from.
            
            Returns:
                str: The description of the company.
        """
        company_description = company_card.find('p', class_='company-description')
        return company_description.text.strip()

    def _extract_company_size(self, company_card: BeautifulSoup) -> CompanySize:
        """ Extracts the size of the company from the company card.

            Args:
                company_card (BeautifulSoup): The company card to extract the size from.
            
            Returns:
                int: The size of the company.
        """
        size_section = company_card.find('ul', class_='location-employees-benefits')
        sections: typing.List[BeautifulSoup] = size_section.find_all('li')
        size_text: str = sections[1].find('span').text.strip()

        return int(size_text.split(' ')[0])

    def _extract_company_location(self, company_card: BeautifulSoup) -> CompanySize:
        """ Extracts the location of the company from the company card.

            Args:
                company_card (BeautifulSoup): The company card to extract the location from.
            
            Returns:
                str: The location of the company.
        """
        location_section = company_card.find('ul', class_='location-employees-benefits')
        sections: typing.List[BeautifulSoup] = location_section.find_all('li')
        location: str = sections[0].find('span').text.strip()

        return location

    def _extract_company_url(self, company_card: BeautifulSoup) -> str:
        """ Extracts the url of the company from the company card.

            Args:
                company_card (BeautifulSoup): The company card to extract the url from.
            
            Returns:
                str: The url of the company.
        """
        company_url = company_card.find('h2', class_='company-name')
        url = company_url.find('a')['href']
        return url

    def _extract_company(self, company_card: BeautifulSoup) -> models.Company:
        """ Extracts the company from the company card.

            Args:
                company_card (BeautifulSoup): The company card to extract the company from.
            
            Returns:
                Company: The company.
        """
        name = self._extract_company_name(company_card)
        industries = self._extract_company_industries(company_card)
        description = self._extract_company_description(company_card)
        size = self._extract_company_size(company_card)
        location = self._extract_company_location(company_card)
        url = '' # self._extract_company_url(company_card)

        return models.Company(name=name,
                       description=description,
                       size=size,
                       location=location,
                       industries=industries,
                       url=url)

    def get_companies(self,
                      sizes: typing.Optional[typing.List[CompanySize]] = None,
                      locations: typing.Optional[typing.List[Location]] = None,
                      timeout: int = 5,
                      max_companies: typing.Optional[int] = None) -> typing.List[models.Company]:
        """ Gets companies from builtin.com.

            Args:
                sizes (typing.Optional[typing.List[CompanySize]]): The sizes of the companies to fetch.
                locations (typing.Optional[typing.List[Location]]): The locations of the companies to fetch.
                timeout (int): The timeout for fetching the companies.

            Returns:
                typing.List[Company]: The companies fetched.
        """
        url = self._generate_companies_url(sizes, locations)
        companies: typing.List[models.Company] = []

        driver = webdriver.Chrome()
        driver.get(url)

        while len(companies) < max_companies if max_companies else True:
            try:
                WebDriverWait(driver, timeout).until(lambda x: x.find_element(By.CLASS_NAME, 'company-card'))
                # TODO: Need to figure out how to wait for the page to load before continuing
                time.sleep(2)
            except TimeoutException:
                print("Timed out waiting for page to load")
            finally:
                print("Page loaded")

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            try:
                company_cards: typing.List[BeautifulSoup] = soup.find_all('section', class_='company-card')
                page_companies = [self._extract_company(company_card) for company_card in company_cards]
                companies.extend(page_companies)
            except Exception as e:
                print(e)
                break

            try:
                driver.find_element(By.CSS_SELECTOR, 'li.page-next').find_element(By.CSS_SELECTOR, 'a').click()
            except:
                break

        driver.close()

        return companies
