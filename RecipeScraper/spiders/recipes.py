import scrapy
from urllib.parse import urljoin


class Recipe():
    categories = ['beef','pork','poultry','lamb','vegetables','seafood','wild-game','baked-goods','cocktails']
    def __init__(self,names:list,urls:list,response_url:str) -> None:
        self.names = names 
        self.urls = urls
        self.response_url = response_url
        self.category = self._find_category()

    def _find_category(self):
        for c in self.categories:
            if c in self.response_url:
                return c 

def make_urls(categories) -> list:
    for c in categories:
        url_str = f"https://www.traeger.com/recipes/{c}?page=1"
        yield url_str


class RecipesSpider(scrapy.Spider):
    name = 'recipes'
    allowed_domains = ['traeger.com']
    base_url = 'https://www.traeger.com'
    categories = ['beef','pork','poultry','lamb','vegetables','seafood','wild-game','baked-goods','cocktails']
    # start_urls = ['https://www.traeger.com/recipes/cocktails?page=1']
    start_urls = list(make_urls(categories))


    def parse(self, response):
        # recipe_names = response.css('.jsx-161492523::text').extract()
        # recipe_urls = response.css('.pt-5 a::attr(href)').getall()
        recipe_names = response.css('.css-mszspu::text').extract()
        recipe_urls = response.css('.css-qh8xft a::attr(href)').getall()

        recipe_urls_modified = []
        for ru in recipe_urls:
            temp_url = str(self.base_url) + str(ru)
            recipe_urls_modified.append(temp_url)

        recipes = Recipe(recipe_names,recipe_urls_modified,response.url)
        rec_category = recipes.category
        return_dict = {} 
        return_dict[rec_category] = {}
        
        for recipe, recipe_url in zip(recipe_names,recipe_urls_modified):
            return_dict[rec_category][recipe] = recipe_url 
        yield return_dict

        next_response = response.css('.css-1rgsgyv')
        
        if len(next_response) != 0:
            next_url = urljoin(response.url,next_response.attrib['href'])
            yield scrapy.Request(next_url,callback = self.parse)
        
