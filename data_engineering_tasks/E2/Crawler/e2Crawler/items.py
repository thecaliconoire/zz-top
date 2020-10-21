import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose


def remove_whitespace(text):
    text = text.replace(' ', '')
    return text
   
def remove_hyphen(hyphen):
     hyphen = hyphen.replace(' - ', '')
     return hyphen

class E2CrawlerItem(scrapy.Item):
    manufacturer = scrapy.Field(input_processor = MapCompose(remove_whitespace))
    category = scrapy.Field(input_processor = MapCompose(remove_whitespace))
    model = scrapy.Field(input_processor = MapCompose(remove_whitespace))
    part = scrapy.Field(input_processor = MapCompose(remove_hyphen))
    part_category = scrapy.Field(input_processor = MapCompose(remove_hyphen))
 
