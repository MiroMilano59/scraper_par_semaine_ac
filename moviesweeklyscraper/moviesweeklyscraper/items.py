# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MoviesweeklyscraperItem(scrapy.Item):
    title = scrapy.Field()
    original_title = scrapy.Field()
    year = scrapy.Field()
    press_score = scrapy.Field()
    spectator_score = scrapy.Field()
    duration = scrapy.Field()
    gender = scrapy.Field()
    director = scrapy.Field()
    public = scrapy.Field()
    nationality = scrapy.Field()
    description = scrapy.Field()
    distributor = scrapy.Field()
    production_year = scrapy.Field()
    actors = scrapy.Field()
    # scriptwriter = scrapy.Field()