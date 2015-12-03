# -*- coding: utf-8 -*-

import json
import psycopg2


class EqPipeline(object):
    def process_item(self, item, spider):
        return item


class irscPipeline(object):
    def __init__(self):

        self.connection = psycopg2.connect(host='localhost', database='EarthQuake', user='postgres')
        self.cursor = self.connection.cursor()

    def process_item(self, item, IrscSpider):
        try:

            self.cursor.execute('''INSERT INTO "EQ_Analyzer_earthquake" ("Origin_Time","Magnitude","Latitude","Longitude","Depth","Region") VALUES (%s,%s,%s,%s,%s,%s)''',
                        (item.get('Origin_Time'), item.get('Magnitude'), item.get('Latitude'), item.get('Longitude'),
                         item.get('Depth'), item.get('Region')))
            self.connection.commit()
            self.cursor.fetchall()

        except psycopg2.DatabaseError, e:
            print "Error: %s" % e
        return item


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('Yeilditems.json', 'wb')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item