# Data Source

![Website Air Quality](../README/Web%20Air-Quality.png)

The data was scraped from https://air-quality.com/
Notes before scraping:

1. Always try to check robots.txt by adding /robots.txt by the end of link. This way, you can check the rule for robots set by the site owner and sitemap of those maps which could save you some time and effort to look up the link for each item you want to scrape.

2. Try to look up for the site API in which the data was taken from. By using API, we could directly access the same data as the one those site takes its data from.

3. Some site stored its data inside a shadow DOM or use JavaScript, most libraries and modules doesn’t have the capabilities to access those data directly which may cause your bots to return different values than what is shown or even an error.

# Method

This document was created by following the tutorials written on scrapy documentation, for more info, please access scrapy documentation [here](https://docs.scrapy.org/en/latest/index.html). Therefore, things that was already explained in tutorial section wouldn’t be written in this document.

## Create Project

To create a project, enter a directory where you’d like to store your code and run:

```
scrapy startproject projectname
```

## Define Item Field

First of all, define the item container by putting this script inside [item.py](AirQuality/AirYogya/items.py)

```
import scrapy

class AiryogyaItem(scrapy.Item):
    time = scrapy.Field()
    place = scrapy.Field()
    aqi = scrapy.Field()
    temperature = scrapy.Field()
    humidity = scrapy.Field()
    wind = scrapy.Field()
    uv = scrapy.Field()
    PM25 = scrapy.Field()
    PM10 = scrapy.Field()
    O3 = scrapy.Field()
    CO = scrapy.Field()
    NO2 = scrapy.Field()
    SO2 = scrapy.Field()
```

This will create item class which is a simple container used to collect the scraped data.

## Spider

This is the script inside the main spider ([Spider.py](AirQuality/AirYogya/spiders/Spider.py))

```
import scrapy

from datetime import datetime
from AirYogya.items import AiryogyaItem

class SpiderSpider(scrapy.Spider):
    name = 'aqual'
    
    def start_requests(self):
        urls = ['https://air-quality.com/place/indonesia/yogyakarta/e892ae41?lang=en&standard=aqi_us',
                'https://air-quality.com/place/indonesia/prambanan/c565a4d1?lang=en&standard=aqi_us',
                'https://air-quality.com/place/indonesia/wates/a44ac0c9?lang=en&standard=aqi_us',
                'https://air-quality.com/place/indonesia/special-region-of-yogyakarta/0e656c5e?lang=en&standard=aqi_us']
        for url in urls:
            yield scrapy.Request(url, self.parse)
    
    def parse(self, response):
        item = AiryogyaItem()
        item["place"] = response.xpath('/html/body/div[1]/div[3]/div[1]/h2/text()').get()
        item["aqi"] = response.xpath('//*[@id="chartBox"]/div[2]/text()').get()
        item["temperature"] = response.xpath('/html/body/div[1]/div[3]/div[5]/div[3]/div[1]/div[2]/text()').get(0)
        item["humidity"] = response.xpath('/html/body/div[1]/div[3]/div[5]/div[3]/div[2]/div[2]/text()').get(0)
        item["wind"] = response.xpath('/html/body/div[1]/div[3]/div[5]/div[3]/div[3]/div[2]/text()').get(0)
        item["uv"] = response.xpath('/html/body/div[1]/div[3]/div[5]/div[3]/div[4]/div[2]/text()').get(0)
        pol1 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[1]/div[1]/text()').get(0)
        pol2 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[2]/div[1]/text()').get(0)
        pol3 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[3]/div[1]/text()').get(0)
        pol4 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[4]/div[1]/text()').get(0)
        pol5 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[5]/div[1]/text()').get(0)
        pol6 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[6]/div[1]/text()').get(0)
        res1 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[1]/div[3]/text()').get(0)
        res2 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[2]/div[3]/text()').get(0)
        res3 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[3]/div[3]/text()').get(0)
        res4 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[4]/div[3]/text()').get(0)
        res5 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[5]/div[3]/text()').get(0)
        res6 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[6]/div[3]/text()').get(0)
        now = datetime.now()
        item["time"] = now.strftime("%Y/%m/%d %H:%M")
        yield item
```
1. ```name```: identifies the Spider. It must be unique within a project, that is, you can’t set the same name for different Spiders.
2. ```start_requests()```: must return an iterable of Requests (you can return a list of requests or write a generator function) which the Spider will begin to crawl from. Subsequent requests will be generated successively from these initial requests.
3. ```parse()```: a method that will be called to handle the response downloaded for each of the requests made. The response parameter is an instance of TextResponse that holds the page content and has further helpful methods to handle it.
4. ```AiryogyaItem()```: this part is an item loader. It provides a convenient mechanism for populating scraped Items.

The ideal way to get a response is by calling its class name, but a lot of site doesn’t really use class name or maybe some item in the same page use the same class name which is why in this case we use xpath. The problem is, since the same class name was used, the order in which item showed up would change sometime, which is why we check the item name so the item inside the dataset match with the header.

## Pipelines

For [pipelines.py](AirQuality/AirYogya/pipelines.py)

```
from datetime import datetime

# insert credential

class AiryogyaPipeline(object):
        
    def process_item(self, item, spider):
        # insert to table
        now = datetime.now()
        time = now.strftime("%Y/%m/%d %H:%M")
        if errors == []:
            print(time, "New rows have been added.")
        else:
            print(time, "An error have been encountered")
        return item
```

The main function in pipelines.py should look like this. To run it just run.

```
scrapy crawl quotes
```

In case you want to store the scraped data directly into a database, just enter the credential or maybe even user and password in “insert credential” placeholder. Also, you have to manually put the item loader in order, each database libraries for python have their own script but most of them usually have a table part that looks like this.

```
(
    item.get('time'),
    item.get('place'),
    item.get('aqi'),
    item.get('temperature'),
    item.get('humidity'),
    item.get('wind'),
    item.get('uv'),
    item.get('PM25'),
    item.get('PM10'),
    item.get('O3'),
    item.get('CO'),
    item.get('NO2'),
    item.get('SO2')
)
```

Put the script above into the script prepared by the database libraries that you use into “insert to table” placeholder.

# Result

![Result](../README/Result%20Air-Quality.png)