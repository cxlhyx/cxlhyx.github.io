import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    """
        def start_requests(self):
            target_url_list = []
            for url in target_url_list:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse
                )
    """

    # 通过重写start_requests方法采用基于方法的多线程

    def parse(self, response):
        pass
