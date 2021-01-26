import scrapy
from datetime import datetime as dt 

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    
    def start_requests(self):
        urls = ['https://air-quality.com/place/indonesia/yogyakarta/e892ae41?lang=en&standard=aqi_us',
                'https://air-quality.com/place/indonesia/prambanan/c565a4d1?lang=en&standard=aqi_us',
                'https://air-quality.com/place/indonesia/wates/a44ac0c9?lang=en&standard=aqi_us']
        for url in urls:
            yield scrapy.Request(url, self.parse)
    
    def parse(self, response):
        place = response.xpath('/html/body/div[1]/div[3]/div[1]/h2/text()').get()
        aqi = response.xpath('//*[@id="chartBox"]/div[2]/text()').get()
        temperature = response.xpath('/html/body/div[1]/div[3]/div[5]/div[3]/div[1]/div[2]/text()').get()
        humidity = response.xpath('/html/body/div[1]/div[3]/div[5]/div[3]/div[2]/div[2]/text()').get()
        wind = response.xpath('/html/body/div[1]/div[3]/div[5]/div[3]/div[3]/div[2]/text()').get()
        uv = response.xpath('/html/body/div[1]/div[3]/div[5]/div[3]/div[4]/div[2]/text()').get()
        pol1 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[1]/div[1]/text()').get() + ' : ' + response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[1]/div[3]/text()').get()
        pol2 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[2]/div[1]/text()').get() + ' : ' + response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[2]/div[3]/text()').get()
        pol3 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[3]/div[1]/text()').get() + ' : ' + response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[3]/div[3]/text()').get()
        pol4 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[4]/div[1]/text()').get() + ' : ' + response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[4]/div[3]/text()').get()
        pol5 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[5]/div[1]/text()').get() + ' : ' + response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[5]/div[3]/text()').get()
        pol6 = response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[6]/div[1]/text()').get() + ' : ' + response.xpath('/html/body/div[1]/div[3]/div[4]/div[2]/div[6]/div[3]/text()').get()
        now = dt.now()
        time = now.strftime("%Y/%m/%d %H:%M")

        yield {
            'date_time': time,
            'Place': place,
            'AQI': aqi,
            'Temperature': temperature,
            'Humidity': humidity,
            'Wind': wind,
            'UV': uv,
            'Pollutant_1': pol1,
            'Pollutant_2': pol2,
            'Pollutant_3': pol3,
            'Pollutant_4': pol4,
            'Pollutant_5': pol5,
            'Pollutant_6': pol6,
        }
