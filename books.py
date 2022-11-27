import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging
from scrapy.crawler import CrawlerRunner


class Books(scrapy.Spider):
    name = 'books'
    start_urls = [
        'https://books.toscrape.com/catalogue/page-1.html'
    ]

    
    def parse(self, response):
        links = response.xpath('//div[@class="image_container"]/a/@href')
        for link in links:
            yield response.follow(link.get(), callback=self.parse_livros)
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            abs_url = f"https://books.toscrape.com/catalogue/{next_page}"
        yield scrapy.Request(
            url=abs_url,
            callback=self.parse
        )

    def parse_livros(self, response):
        dados = response.xpath('//div[@class="col-sm-6 product_main"]')
        avaliacao = dados.xpath('(.//p/@class)[last()]').get()
        if avaliacao == 'star-rating One':
            avaliacao = '1'
        if avaliacao == 'star-rating Two':
            avaliacao = '2'
        if avaliacao == 'star-rating Three':
            avaliacao = '3'
        if avaliacao == 'star-rating Four':
            avaliacao = '4'
        if avaliacao == 'star-rating Five':
            avaliacao = '5'
        
        estoque = dados.xpath('(.//p[@class="instock availability"]/text())[last()]').get().replace("\n", "").strip().replace('In stock (','').replace(' available)','')

        yield {
            'livro':str(dados.xpath('.//h1/text()').get().replace('"',"'")),
            'categoria':str(response.xpath('(//li/a)[last()]/text()').get()),
            'estrelas':int(avaliacao),
            'preco':float(dados.xpath('.//p[@class="price_color"]/text()').get().replace("£", "")),
            'estoque':int(estoque)
        }

def run():
    process = CrawlerProcess(settings= {
            'USER_AGENT' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            "FEEDS": {"books.csv": {"format": "csv", "overwrite": True}},
        })
    process.crawl(Books)
    process.start()

if __name__ == "__main__":
    run()