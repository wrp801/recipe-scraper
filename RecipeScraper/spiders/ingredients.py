import scrapy
import pandas as pd 
import os 

def make_urls(filename:str) -> list:
    current_wd = os.getcwd()
    filepath = os.path.join(current_wd,'Recipes','spiders','OutputData',filename)
    df = pd.read_csv(filepath)
    urls = df['Urls'].tolist()
    return urls



class IngredientsSpider(scrapy.Spider):
    name = 'ingredients'
    allowed_domains = ['traeger.com']
    start_urls = make_urls("Results.csv")

    def parse(self, response):
        ingredients = response.xpath('//*[@id="__next"]/div/div[3]/div[3]/div[2]/div/div[1]/div').css('span::text').extract()
        url = response.url
        yield {url:ingredients}

