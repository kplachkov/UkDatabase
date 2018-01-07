# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from bs4 import BeautifulSoup


class UkDatabaseSpider(scrapy.Spider):
    """Crawl the entire web site"""

    name = "uk_database_site"
    """str: The name of the spider."""
    allowed_domains = ['theukdatabase.com']
    """list: Allowed domains to crawl."""
    start_urls = ['http://theukdatabase.com/']
    """list: The URLs to start crawling from."""

    def parse(self, response):
        """Generator for parsing a page.
        Args:
            response: Web page.
        Yields:
            dict: The scraped information.
            class: scrapy.Request for the next pages.
        """

        links_selector: str = "a ::attr(href)"  # The scrapy selector for links.

        post_title = self.__get_post_title(response)
        post_text = self.__get_post_text(response)
        post_pub_date: datetime = self.__get_post_pub_date(response)
        post_images_src = self.__get_post_images(response)
        if post_title or post_text or post_images_src:
            yield {
                "TITLE": post_title,
                "TEXT": post_text,
                "POST_PUB_DATE": post_pub_date,
                "IMAGES": post_images_src,
            }

        links = response.css(links_selector).extract()
        # Continues with scraping all the links from the current page.
        for link in links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse
            )

    @staticmethod
    def __get_post_title(response) -> str:
        """Get the post title.
        Args:
            response: Web page.
        Returns:
            str: The post title.
        """
        try:
            return response.xpath("//header[@class = 'post-title']/h1/text()").extract_first()
        except Exception as e:
            print("Exception:", e)

    @staticmethod
    def __get_post_pub_date(response) -> datetime:
        """Get the post published date.
        Args:
            response: Web page.
        Returns:
            datetime: The post published date.
        """
        try:
            post_date_html: str = response.xpath("//p[@class = 'post-date']").extract_first()
            if post_date_html:
                post_date_soup = BeautifulSoup(post_date_html)
                date: str = post_date_soup.find("strong").contents[0]
                # day_of_the_week: str = post_date_soup.find("em").contents[0]
                month_and_year: str = post_date_soup.find("span").contents[0]
                date_str = "{} {}".format(date, month_and_year)
                post_date = datetime.strptime(date_str, "%d %b %Y")
                return post_date
        except Exception as e:
            print("Exception:", e)

    @staticmethod
    def __get_post_text(response) -> str:
        """Get the post text.
        Args:
            response: Web page.
        Returns:
            str: The post text.
        """
        try:
            post_html: str = response.xpath("//div[@class = 'post-entry']").extract_first()
            if post_html:
                advertisements_html: str = response \
                    .xpath("//div[@class = 'post-entry']//div[@class = 'wpcnt']") \
                    .extract_first()
                unnecessary_scripts_html: str = response \
                    .xpath("//div[@class = 'post-entry']//div[@id = 'atatags-335202795']") \
                    .extract_first()
                related_posts_html: str = response \
                    .xpath("//div[@class = 'post-entry']//div[@id = 'jp-post-flair']") \
                    .extract_first()
                # Removes the advertisements, scripts and related posts text.
                if advertisements_html:
                    post_html = post_html.replace(advertisements_html, "")
                if unnecessary_scripts_html:
                    post_html = post_html.replace(unnecessary_scripts_html, "")
                if related_posts_html:
                    post_html = post_html.replace(related_posts_html, "")
                post_text_soup = BeautifulSoup(post_html)
                post_text_list: list = post_text_soup.findAll(text=True)  # Takes the text from the html code.
                post_text_list_cleared: list = list(filter("\n".__ne__, post_text_list))  # Remove the "\n".
                post_text = " ".join(post_text_list_cleared)
                return post_text
        except Exception as e:
            print("Exception:", e)

    @staticmethod
    def __get_post_images(response) -> list:
        """Get the post images.
        Args:
            response: Web page.
        Returns:
            list: The images from the post.
        """
        try:
            return response.xpath("//div[@class = 'post-entry']//img/@src").extract()
        except Exception as e:
            print("Exception:", e)
