import scrapy


from pep_parse.items import PepParseItem
from pep_parse.settings import ALLOWED_DOMAINS, PEP, START_URL


class PepSpider(scrapy.Spider):
    name = PEP
    allowed_domains = ALLOWED_DOMAINS
    start_urls = START_URL

    def parse(self, response):
        pep_list = response.css(
            '#numerical-index table.pep-zero-table tbody tr'
        )
        for pep in pep_list:
            pep_link = pep.css('a::attr(href)').get()
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        h1 = response.css('#pep-content > h1::text').get().split()
        number = h1[1]
        name = ' '.join(h1[3:])
        status = response.css('abbr::text').get()
        context = {
            'number': number,
            'name': name,
            'status': status
        }
        yield PepParseItem(context)
