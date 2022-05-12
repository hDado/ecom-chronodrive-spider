# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class EcommercePipeline(object):
    def open_spider(self,spider):

        self.connection = sqlite3.connect("chronodrive.db")
        self.c = self.connection.cursor()
        try:
               self.c.execute('''
                    CREATE TABLE ChProd(
                        product_description TEXT,
                        quantity_weight TEXT,
                        price REAL,
                        link TEXT
                        )

    
                ''')
        except sqlite3.OperationalError:
            pass
    

            self.connection.commit()

    def close_spider(self,spider):
        self.connection.close()    

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO ChProd(product_description,quantity_weight,price,link) VALUES(?,?,?,?)

            ''', (  
                item.get("product_description"),
                item.get("quantity_weight"),
                item.get("price"),
                item.get("product_link")
        ))
        self.connection.commit()        
        
        return item

class PostgresPipeline(object):

    pass