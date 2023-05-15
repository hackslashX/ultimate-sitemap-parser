from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

import os
import time
import random
import string
from typing import Optional, Dict
from http import HTTPStatus

from .abstract_client import (
    AbstractWebClient,
    AbstractWebClientSuccessResponse,
    WebClientErrorResponse,
)
from usp.__about__ import __version__


class UndetectedChromiumClientSuccessResponse(AbstractWebClientSuccessResponse):
    """
    requests-based successful response.
    """

    __slots__ = [
        '__requests_response',
        '__max_response_data_length',
    ]

    def __init__(self, requests_response, max_response_data_length: Optional[int] = None):
        self.__requests_response = requests_response
        self.__max_response_data_length = max_response_data_length
    
    def status_code(self) -> int:
        return int(self.__requests_response['status_code'])
    
    def status_message(self) -> str:
        message = HTTPStatus(self.status_code(), None).phrase
        return message

    def header(self, case_insensitive_name: str) -> Optional[str]:
        if case_insensitive_name.lower() == 'content-type':
            return self.__requests_response['content-type']
        return None
    
    def raw_data(self) -> bytes:
        if self.__max_response_data_length:
            data = self.__requests_response['content'][:self.__max_response_data_length]
        else:
            data = self.__requests_response['content']

        if 'gzip' not in self.__requests_response['content-type']:
            data = data.encode('utf-8')

        return data


class UndetectedChromiumClientErrorResponse(WebClientErrorResponse):
    """
    requests-based error response.
    """
    pass


class UndetectedChromiumClient(AbstractWebClient):

    """requests-based web client to be used by the sitemap fetcher."""

    __USER_AGENT = 'ultimate_sitemap_parser/{}'.format(__version__)

    __HTTP_REQUEST_TIMEOUT = 60
    """
    HTTP request timeout.

    Some webservers might be generating huge sitemaps on the fly, so this is why it's rather big.
    """

    __slots__ = [
        '__max_response_data_length',
        '__timeout',
        '__proxies',
    ]

    def __init__(self):
        self.__max_response_data_length = None
        self.__timeout = self.__HTTP_REQUEST_TIMEOUT
        self.__proxies = {}
    
    def get_undetected_chromium_flag(self):
        return True
    
    def get_chrome_options(self):
        # Create undetected chromedriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        # Change download location
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        self.__download_location = "./smd/" + random_string

        # Delete folder if it exists
        if os.path.exists(self.__download_location):
            os.rmdir(self.__download_location)
        
        # Create folder
        os.makedirs(self.__download_location)

        # User agent
        #chrome_options.add_argument(f"--user-agent={self.__USER_AGENT}")

        # prefs = {"download.default_directory" : self.__download_location}
        # chrome_options.add_experimental_option("prefs", prefs)

        return chrome_options
    
    def get_driver(self):
        return uc.Chrome(options=self.get_chrome_options())

    
    def set_timeout(self, timeout: int) -> None:
        """Set HTTP request timeout."""
        # Used mostly for testing
        self.__timeout = timeout

    def set_proxies(self, proxies: Dict[str, str]) -> None:
        """
        Set proxies from dictionnary where:

        * keys are schemes, e.g. "http" or "https";
        * values are "scheme://user:password@host:port/".
        
        For example:

            proxies = {'http': 'http://user:pass@10.10.1.10:3128/'}
        """
        # Used mostly for testing
        self.__proxies = proxies
    
    def set_max_response_data_length(self, max_response_data_length: int) -> None:
        self.__max_response_data_length = max_response_data_length
    
    def get(self, url: str, driver):
        result = {
            "status_code": 200,
            "content": None,
            "content-type": "text/html",
        }
        self.__driver = driver
        try:
            current_file_count = len(os.listdir(self.__download_location))
            self.__driver.get(url)
            counter = 0
            # If page title == "Just a moment..." then it's a CF page, wait
            while self.__driver.title == "Just a moment..." or counter == 25:
                time.sleep(1)
                counter += 1
            # Detect if a file was downloaded, and if page source is empty
            page_source = self.__driver.page_source
            new_file_count = len(os.listdir(self.__download_location))
            if new_file_count > current_file_count and page_source == "":
                # Get file name
                file_name = os.listdir(self.__download_location)[0]
                # Get file path
                file_path = self.__download_location + "/" + file_name
                # Read file
                with open(file_path, 'r') as file:
                    data = file.read()
                # Delete file
                os.remove(file_path)
                # If extension is gzip or zip set content type
                if file_name.endswith(".gz") or file_name.endswith(".zip") or file_name.endswith(".gzip"):
                    result["content-type"] = "application/gzip"
                # Set result
                result["content"] = data
            else:
                # Append view-source: to url
                url = "view-source:" + url
                self.__driver.get(url)
                page_source = self.__driver.find_element(By.XPATH, "/html/body").text.strip()
                # Remove first line
                if page_source.split("\n", 1)[0].startswith("Line"):
                    page_source = page_source.split("\n", 1)[1]
                result["content"] = page_source
                if "<?xml" in page_source:
                    result["content-type"] = "application/xml"
                if "<html" in page_source:
                    result["content-type"] = "text/html"
                    result["content"] = ""
        except Exception as e:
            result["status_code"] = 500
            result["content"] = str(e)
            print(e)
        else:
            if result['status_code'] == 200:
                return UndetectedChromiumClientSuccessResponse(
                    requests_response=result,
                    max_response_data_length=self.__max_response_data_length,
                )

        return UndetectedChromiumClientErrorResponse(
            message='failed', retryable=False
        )
