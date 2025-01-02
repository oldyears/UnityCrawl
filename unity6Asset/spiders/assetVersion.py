import scrapy
import json
import re
from unity6Asset.items import Unity6AssetItem

class AssetSpider(scrapy.Spider):
    name = 'asset_version'
    allowed_domains = ['assetstore.unity.com']
    base_url = 'https://assetstore.unity.com/packages/'
    start_urls = ['https://assetstore.unity.com/?category=3d&release=180&version=6000&orderBy=1&page=0&rows=96']
    # start_urls = ['https://assetstore.unity.com/packages/2d/gui/text-effects-300630']
    # start_urls = ['https://assetstore.unity.com/?category=2d%5C3d%5Cadd-ons%5Caudio%5Cessentials%5Ctemplates%5Ctools%5Cvfx&version=6000&release=31&orderBy=1&page=0&rows=96']

    def start_requests(self):
        with open("2dUrls.json", 'r') as file:
            assets = json.load(file)

        i = 0
        for asset in assets:
            url = asset['url']
            yield scrapy.Request(url, callback=self.parse, meta={"data":asset})
            i += 1
            if i % 100 == 0:
                print(i)

    def parse(self, response):
        # 提取商品的 Original Unity version 信息
        items = response.meta['data']
        items['unityVersion'] = response.xpath('//div[contains(@class, "product-support_version")]//div[@class="SoNzt"]/text()[normalize-space()]').get()
        
        # add a test to unity6
        if "6000" in items['unityVersion']:
            yield items
