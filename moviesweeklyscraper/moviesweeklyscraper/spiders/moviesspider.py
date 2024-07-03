import scrapy
from moviesweeklyscraper.items import MoviesweeklyscraperItem
import datetime
from datetime import timedelta

class MoviesspiderSpider(scrapy.Spider):
    name = "moviesspider"
    allowed_domains = ["allocine.fr"]

    def start_requests(self):
        start_date = datetime.date(2024, 7, 3)
        nb_semaine_max = 4  # en vrai je peux passer à 50
        for i in range(nb_semaine_max):
            date_str = (start_date + timedelta(weeks=i)).strftime("%Y-%m-%d")
            url = f"https://www.allocine.fr/film/agenda/sem-{date_str}/"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        movies = response.xpath("//li[@class='mdl']")

        for movie in movies:
            movie_url = movie.xpath(".//div/h2/a/@href").get()
            if movie_url:
                yield response.follow(movie_url, callback=self.parse_movie)

        # Pagination : récupérer l'URL de la page suivante
        next_page = response.xpath(".//a[@class='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_movie(self, response):
        item = MoviesweeklyscraperItem()
        item['title'] = response.xpath("//div[@class='titlebar titlebar-page']/div/text()").get()
        item['original_title'] = response.xpath("//div[@class='meta-body-item']/span/text()").getall()
        item['year'] = response.xpath("//div[@class='meta-body-item meta-body-info']/span/text()").get()
        item['press_score'] = response.xpath("//div[@class='rating-item']/div/div/span/text()").get()
        item['spectator_score'] = response.xpath("//div[@class='rating-item'][2]//span[@class='stareval-note']/text()").get()
        item['duration'] = response.xpath("//div[@class='meta-body-item meta-body-info']/text()").getall()
        item['gender'] = response.xpath("//span[@class='spacer']/following-sibling::span/text()").getall()
        # item['director'] = response.xpath("//div[@class='meta-body-item meta-body-direction meta-body-oneline']/span/text()").getall()
        item['public'] = response.xpath("//div[@class='certificate']/span[@class='certificate-text']/text()").get()
        item['nationality'] = response.xpath("//section[@class='section ovw ovw-technical']/div/span/span/text()").getall()
        item['description'] = response.xpath("//p[@class='bo-p']/text()").getall()
        item['distributor'] = response.xpath("//section[@class='section ovw ovw-technical']/div[3]/span/text()").getall()
        item['production_year'] = response.xpath("//section[@class='section ovw ovw-technical']/div[4]/span/text()").getall()

        casting_url = response.url.replace('_gen_cfilm=', '-').replace('.html', '/casting/')
        yield scrapy.Request(casting_url, meta={'item': item}, callback=self.parse_casting)

    def parse_casting(self, response):
        item = response.meta['item']
        actors = response.xpath("//section[@class='section casting-actor']/div/div/div/div/a/text()").getall()
        item['actors'] = [actor.strip() for actor in actors if actor.strip()]
        directors = response.xpath("//section[@class='section casting-director']/div[2]//div/a/text()").getall()
        item['director'] = [director.strip() for director in directors if director.strip()]
        # scriptwriters = response.xpath("//section[@class='section casting-director']/div[2]//div/a/text()").getall()
        # item['scriptwriter'] = [scriptwriter.strip() for scriptwriter in scriptwriters if scriptwriter.strip()]
        # yield item
