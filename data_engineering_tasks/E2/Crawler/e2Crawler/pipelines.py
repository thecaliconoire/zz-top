

# class E2CrawlerPipeline(object):
#     def process_item(self, item, spider):
        # item['task_id'] = task_id
        # if col is not None:
        #     if any(item.values()):
        #         col.save(item)
        #         return item
        #     else:
        #         raise DropItem()

# class CsvPipeline(object):
#     def __init__(self):
#         self.file = open("booksdata.csv", 'wb')
#         self.exporter = CsvItemExporter(self.file, unicode)
#         self.exporter.start_exporting()

#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()

#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item

