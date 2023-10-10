# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import re

logger = logging.getLogger()

class DogEarSpidersPipeline:
    def __init__(self, *args, **kwargs):
        self

    def close_spider(self, spider): 
        logger.info('--------Closed Spider------- %s')

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## Strip all whitespaces from strings / Strip all HTML tags from description
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()
            else:
                value = adapter.get(field_name)
                adapter[field_name] = re.sub('/<([^>]+)>/', '', value)

        # custom title case function that handles apostrophes
        def title_case(s):
            return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                            lambda mo:
                            mo.group(0)[0].upper() +
                            mo.group(0)[1:].lower(), s)
        
        ## Use title_case function
        title_case_keys = ['title', 'author']
        for title_case_key in title_case_keys:
            value = adapter.get(title_case_key)
            adapter[title_case_key] = title_case(value)
        
        logger.info('--------Parsed items------- %s', item)
        return item