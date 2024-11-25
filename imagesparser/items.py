# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImagesparserItem(scrapy.Item):
    title = scrapy.Field()      # Название изображения
    url = scrapy.Field()        # URL изображения
    category = scrapy.Field()   # Категория
    images = scrapy.Field()     # Поле для ImagesPipeline
    image_urls = scrapy.Field()
