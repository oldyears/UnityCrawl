# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class Unity6AssetPipeline:
    def process_item(self, item, spider):
        return item
    
class SaveToJsonPipeline:
    def __init__(self):
        self.buffer = []
        self.buffer_size = 100
        self.file = open("unity6Asset2D.json", 'w', encoding='utf-8')
        self.file.write('[\n')
    
    def process_item(self, item, spider):
        self.buffer.append(item)

        if len(self.buffer) >= self.buffer_size:
            self.flush_to_json()

        return item
    
    def flush_to_json(self):
        for i, item in enumerate(self.buffer):
            if i > 0:
                self.file.write(',\n')
            json.dump(item, self.file, ensure_ascii=False, indent=4)
        
        print("items have written.")
        self.buffer = []
    
    def close_spider(self, spider):
        if self.buffer:
            self.flush_to_json()

        self.file.write('\n]')
        self.file.close()
        print("succuss!")

