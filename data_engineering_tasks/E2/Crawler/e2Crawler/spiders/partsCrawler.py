import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Compose, Join, SelectJmes
from e2Crawler.items import E2CrawlerItem


class PartscrawlerSpider(CrawlSpider):
    name = 'partsCrawler'
    fn = 'www.urparts'
    dn = fn + '.com'
    allowed_domains = [dn]
    start_urls = [
        'https://www.urparts.com/index.cfm/page/catalogue/'     
    ]
    rules = (
        Rule(LinkExtractor(allow=('catalogue')), callback='parse_page', follow=True),
    )

    def parse_page(self, res):
        parts = res.css('div#contentWrapWide')

        for part in parts:
            make_loader = ItemLoader(item = E2CrawlerItem(), selector = part)
            make_loader.default_output_processor = TakeFirst()
            part = {
            make_loader.add_xpath('manufacturer', '//div[@class="c_container allmakes"]/ul/li/a/text()'),
            make_loader.add_css('category', 'div.c_container.allmakes.allcategories a::text'),
            make_loader.add_xpath('model', "//div[@class='c_container allmodels']//ul/li/a/text()"),
            make_loader.add_xpath('part', '//div[@class="c_container allparts"]//ul/li/a/text()'),
            make_loader.add_xpath('part_category', '//div[@class="c_container allparts"]//ul/li/a/span/text()')
            }
            yield make_loader.load_item()