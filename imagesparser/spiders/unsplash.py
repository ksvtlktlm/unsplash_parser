import scrapy
import logging
from imagesparser.items import ImagesparserItem


class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def __init__(self, *args, **kwargs):
        super(UnsplashSpider, self).__init__(*args, **kwargs)
        self.logger.setLevel(logging.DEBUG)

    def parse(self, response):
        categories = response.xpath("//header/following-sibling::div//ul//li/a[@href]/@href").getall()[6:]
        print("Собранные категории:", categories)
        for category in categories:
            absolute_link_category = response.urljoin(category)
            yield response.follow(absolute_link_category, callback=self.parse_category)

    def parse_category(self, response):
        print(f'\nОбрабатываем категорию {response.url.split("/")[-1].upper()}\n')

        photos_elements = response.xpath("//img[@alt and @sizes]")
        for element in photos_elements:
            item = ImagesparserItem()
            item['title'] = element.xpath("@alt").get(default='No title').strip()
            item['url'] = response.urljoin(element.xpath("@src").get())
            item['category'] = response.url.split('/')[-1]
            item['image_urls'] = [item['url']]
            self.logger.debug(f"Item подготовлен: {item}")

            yield item