"""Objects that represent a page found in one of the sitemaps."""

import datetime
from decimal import Decimal
from enum import Enum, unique
from typing import List, Optional

SITEMAP_PAGE_DEFAULT_PRIORITY = Decimal('0.5')
"""Default sitemap page priority, as per the spec."""


class SitemapImage(object):
    __slots__ = [
        '__image_url',
        '__image_title',
        '__image_caption',
    ]

    def __init__(self,
                 image_url: str,
                 image_title: str,
                 image_caption: Optional[str] = None):
        self.__image_url = image_url
        self.__image_title = image_title
        self.__image_caption = image_caption

    def __eq__(self, other) -> bool:
        if not isinstance(other, SitemapImage):
            raise NotImplemented

        if self.image_url != other.image_url:
            return False

        if self.image_title != other.image_title:
            return False
        
        if self.image_caption != other.image_caption:
            return False

        return True

    def __hash__(self):
        return hash((
            self.image_url,
        ))

    def __repr__(self):
        return (
            "{self.__class__.__name__}("
            "image_title={self.image_title}, "
            "image_url={self.image_url}, "
            "image_caption={self.image_caption}"
            ")"
        ).format(self=self)

    @property
    def image_title(self) -> str:
        """
        Return image title.

        :return: image title.
        """
        return self.__image_title

    @property
    def image_url(self) -> str:
        """
        Return image location.

        :return: image location.
        """
        return self.__image_url

    @property
    def image_caption(self) -> Optional[str]:
        """
        Return image caption.

        :return: image caption.
        """
        return self.__image_caption




class SitemapNewsStory(object):
    """
    Single story derived from Google News XML sitemap.
    """

    __slots__ = [
        '__title',
        '__publish_date',
        '__publication_name',
        '__publication_language',
        '__access',
        '__genres',
        '__keywords',
        '__stock_tickers',
    ]

    def __init__(self,
                 title: str,
                 publish_date: datetime.datetime,
                 publication_name: Optional[str] = None,
                 publication_language: Optional[str] = None,
                 access: Optional[str] = None,
                 genres: List[str] = None,
                 keywords: List[str] = None,
                 stock_tickers: List[str] = None):
        """
        Initialize a new Google News story.

        :param title: Story title.
        :param publish_date: Story publication date.
        :param publication_name: Name of the news publication in which the article appears in.
        :param publication_language: Primary language of the news publication in which the article appears in.
        :param access: Accessibility of the article.
        :param genres: List of properties characterizing the content of the article.
        :param keywords: List of keywords describing the topic of the article.
        :param stock_tickers: List of up to 5 stock tickers that are the main subject of the article.
        """

        # Spec defines that some of the properties below are "required" but in practice not every website provides the
        # required properties. So, we require only "title" and "publish_date" to be set.

        self.__title = title
        self.__publish_date = publish_date
        self.__publication_name = publication_name
        self.__publication_language = publication_language
        self.__access = access
        self.__genres = genres if genres else []
        self.__keywords = keywords if keywords else []
        self.__stock_tickers = stock_tickers if stock_tickers else []

    def __eq__(self, other) -> bool:
        if not isinstance(other, SitemapNewsStory):
            raise NotImplemented

        if self.title != other.title:
            return False

        if self.publish_date != other.publish_date:
            return False

        if self.publication_name != other.publication_name:
            return False

        if self.publication_language != other.publication_language:
            return False

        if self.access != other.access:
            return False

        if self.genres != other.genres:
            return False

        if self.keywords != other.keywords:
            return False

        if self.stock_tickers != other.stock_tickers:
            return False

        return True

    def __hash__(self):
        return hash((
            self.title,
            self.publish_date,
            self.publication_name,
            self.publication_language,
            self.access,
            self.genres,
            self.keywords,
            self.stock_tickers,
        ))

    def __repr__(self):
        return (
            "{self.__class__.__name__}("
            "title={self.title}, "
            "publish_date={self.publish_date}, "
            "publication_name={self.publication_name}, "
            "publication_language={self.publication_language}, "
            "access={self.access}, "
            "genres={self.genres}, "
            "keywords={self.keywords}, "
            "stock_tickers={self.stock_tickers}"
            ")"
        ).format(self=self)

    @property
    def title(self) -> str:
        """
        Return story title.

        :return: Story title.
        """
        return self.__title

    @property
    def publish_date(self) -> datetime.datetime:
        """
        Return story publication date.

        :return: Story publication date.
        """
        return self.__publish_date

    @property
    def publication_name(self) -> Optional[str]:
        """
        Return name of the news publication in which the article appears in.

        :return: Name of the news publication in which the article appears in.
        """
        return self.__publication_name

    @property
    def publication_language(self) -> Optional[str]:
        """Return primary language of the news publication in which the article appears in.

        It should be an ISO 639 Language Code (either 2 or 3 letters).

        :return: Primary language of the news publication in which the article appears in.
        """
        return self.__publication_language

    @property
    def access(self) -> Optional[str]:
        """
        Return accessibility of the article.

        :return: Accessibility of the article.
        """
        return self.__access

    @property
    def genres(self) -> List[str]:
        """
        Return list of properties characterizing the content of the article.

        Returns genres such as "PressRelease" or "UserGenerated".

        :return: List of properties characterizing the content of the article
        """
        return self.__genres

    @property
    def keywords(self) -> List[str]:
        """
        Return list of keywords describing the topic of the article.

        :return: List of keywords describing the topic of the article.
        """
        return self.__keywords

    @property
    def stock_tickers(self) -> List[str]:
        """
        Return list of up to 5 stock tickers that are the main subject of the article.

        Each ticker must be prefixed by the name of its stock exchange, and must match its entry in Google Finance.
        For example, "NASDAQ:AMAT" (but not "NASD:AMAT"), or "BOM:500325" (but not "BOM:RIL").

        :return: List of up to 5 stock tickers that are the main subject of the article.
        """
        return self.__stock_tickers


@unique
class SitemapPageChangeFrequency(Enum):
    """Change frequency of a sitemap URL."""

    ALWAYS = 'always'
    HOURLY = 'hourly'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'
    NEVER = 'never'

    @classmethod
    def has_value(cls, value: str) -> bool:
        """Test if enum has specified value."""
        return any(value == item.value for item in cls)


class SitemapPage(object):
    """Single sitemap-derived page."""

    __slots__ = [
        '__url',
        '__priority',
        '__last_modified',
        '__change_frequency',
        '__news_story',
        '__image'
    ]

    def __init__(self,
                 url: str,
                 priority: Decimal = SITEMAP_PAGE_DEFAULT_PRIORITY,
                 last_modified: Optional[datetime.datetime] = None,
                 change_frequency: Optional[SitemapPageChangeFrequency] = None,
                 news_story: Optional[SitemapNewsStory] = None,
                 image: Optional[SitemapImage] = None):
        """
        Initialize a new sitemap-derived page.

        :param url: Page URL.
        :param priority: Priority of this URL relative to other URLs on your site.
        :param last_modified: Date of last modification of the URL.
        :param change_frequency: Change frequency of a sitemap URL.
        :param news_story: Google News story attached to the URL.
        """
        self.__url = url
        self.__priority = priority
        self.__last_modified = last_modified
        self.__change_frequency = change_frequency
        self.__news_story = news_story
        self.__image = image

    def __eq__(self, other) -> bool:
        if not isinstance(other, SitemapPage):
            raise NotImplemented

        if self.url != other.url:
            return False

        if self.priority != other.priority:
            return False

        if self.last_modified != other.last_modified:
            return False

        if self.change_frequency != other.change_frequency:
            return False

        if self.news_story != other.news_story:
            return False
        
        if self.image != other.image:
            return False

        return True

    def __hash__(self):
        return hash((
            # Hash only the URL to be able to find unique pages later on
            self.url,
        ))

    def __repr__(self):
        return (
            "{self.__class__.__name__}("
            "url={self.url}, "
            "priority={self.priority}, "
            "last_modified={self.last_modified}, "
            "change_frequency={self.change_frequency}, "
            "news_story={self.news_story}, "
            "image={self.image}, "
            ")"
        ).format(self=self)

    @property
    def url(self) -> str:
        """
        Return page URL.

        :return: Page URL.
        """
        return self.__url

    @property
    def priority(self) -> Decimal:
        """
        Return priority of this URL relative to other URLs on your site.

        :return: Priority of this URL relative to other URLs on your site.
        """
        return self.__priority

    @property
    def last_modified(self) -> Optional[datetime.datetime]:
        """
        Return date of last modification of the URL.

        :return: Date of last modification of the URL.
        """
        return self.__last_modified

    @property
    def change_frequency(self) -> Optional[SitemapPageChangeFrequency]:
        """
        Return change frequency of a sitemap URL.

        :return: Change frequency of a sitemap URL.
        """
        return self.__change_frequency

    @property
    def news_story(self) -> Optional[SitemapNewsStory]:
        """
        Return Google News story attached to the URL.

        :return: Google News story attached to the URL.
        """
        return self.__news_story
    
    @property
    def image(self) -> Optional[SitemapImage]:
        """
        Returns Image in Sitemap

        :return: Sitemap image
        """
        return self.__image
