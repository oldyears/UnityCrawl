import scrapy
import json
import re
from unity6Asset.items import Unity6AssetItem

class AssetSpider(scrapy.Spider):
    name = 'asset_spider'
    allowed_domains = ['assetstore.unity.com']
    base_url = 'https://assetstore.unity.com/packages/'
    start_urls = ['https://assetstore.unity.com/?category=2d&release=180&version=6000&orderBy=1&page=0&rows=96']
    # start_urls = ['https://assetstore.unity.com/packages/2d/gui/text-effects-300630']
    # start_urls = ['https://assetstore.unity.com/?category=2d%5C3d%5Cadd-ons%5Caudio%5Cessentials%5Ctemplates%5Ctools%5Cvfx&version=6000&release=31&orderBy=1&page=0&rows=96']

    # extract data
    def extract_search_data(self, script_text):
        try:
            start = script_text.index('\"search\":')
            start = script_text.index('\"results\":[', start) + len('\"results\":')
            end = script_text.index('}],', start) + 2
            search_json = script_text[start:end]
            search_data = json.loads(search_json)
            return search_data
        except (ValueError, IndexError) as e:
            self.logger.error(f"can't extract search data: {e}")
            return None

    def extract_product_url(self, name, id, category):
        slug = name.lower()
        slug = re.sub(r'[^a-z]+', '-', slug)
        slug = slug.strip('-')
        return self.base_url + category + '/' + slug + '-' + id

    def parse(self, response):
        json_data = response.xpath("//script[contains(text(), 'search')]/text()").getall()
        
        search_data = self.extract_search_data(json_data[1])

        if search_data:
            for product in search_data:
                items = Unity6AssetItem()
                items['id'] = product['id']
                items['name'] = product['name']
                items['category'] = product['category']
                items['url'] = self.extract_product_url(product['name'], product['id'], product['category'])
                # yield response.follow(items['url'], callback=self.parse_product, meta={'data':items})
                yield items
            print("success!")

        # 分页处理：如果有下一页，继续抓取
        has_button = response.xpath('//button[@label="Next"]').get()
        has_next = response.xpath('//button[@label="Next"]/@disabled').get()
        if has_next is not None or has_button is None:
            print("all pages have finished")
        else:
            # current_page = int(response.url.split('=')[-1])
            page_index = response.url.index("page=") + len("page=")
            page_index_end = response.url.index("&", page_index)
            current_page =int(response.url[page_index:page_index_end])
            next_page = current_page + 1
            print(f"current page is {current_page}")

            next_url = response.url.replace(f'page={current_page}', f'page={next_page}')
            yield response.follow(next_url, callback=self.parse)

    def parse_product(self, response):
        # 提取商品的 Original Unity version 信息
        items = response.meta['data']
        items['unityVersion'] = response.xpath('//div[contains(@class, "product-support_version")]//div[@class="SoNzt"]/text()[normalize-space()]').get()
        
        # add a test to unity6
        if "6000" in items['unityVersion']:
            yield items
