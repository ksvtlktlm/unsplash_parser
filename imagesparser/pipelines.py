# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter



import csv
from scrapy.exceptions import DropItem

class ImagesparserPipeline:
    def process_item(self, item, spider):
        return item


class CsvExportPipeline:
    def open_spider(self, spider):
        self.file = open('images_data.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file, delimiter=';')
        self.writer.writerow(['Title', 'Category', 'Image URL', 'Local Path'])
        self.seen_urls = set()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        unique_id = item['url']
        if unique_id in self.seen_urls:
            raise DropItem(f"Duplicate item found: {item}")
        self.seen_urls.add(unique_id)

        image_path = item.get('images', [{}])[0].get('path', 'N/A')
        self.writer.writerow([item['title'], item['category'], item['url'], image_path])

        return item