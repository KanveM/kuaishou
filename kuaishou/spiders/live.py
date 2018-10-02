# -*- coding: utf-8 -*-
import sys
import scrapy
import re
from kuaishou.items import KuaishouItem

# #profile
#     liveName = scrapy.Field() #主播名
#     livePhoto = scrapy.Field()#主播照片
#     liveID = scrapy.Field() #主播id
#     liveIntroduce = scrapy.Field() #简介
#     liveSex = scrapy.Field() #性别
#     liveConstellation = scrapy.Field() #星座
#     liveLocation = scrapy.Field() #地区

#     liveFans = scrapy.Field() #粉丝数
#     liveAttention = scrapy.Field() #关注数
#     liveProduction = scrapy.Field() #作品数
class LiveSpider(scrapy.Spider):
    name = 'live'
    allowed_domains = ['live.kuaishou.com']
    start_urls = ['https://live.kuaishou.com/profile/KSG7yyyy/','https://live.kuaishou.com/profile/HYH88888888']

    def parse(self, response):
        def getName(item):
            try:
                item['liveName'] = response.xpath('/html//p[@class="user-info-name"]/text()').extract()
                if type(item['liveName']) is list:
                    item['liveName'] = item['liveName'][0] #如果时list则取其一
                item['liveName'] = str(item['liveName']).strip('\n').strip()
            except Exception as e:
                print('@get name error', e, file=sys.stderr)

        def getID(item):
            try:
                item['liveID'] = response.xpath('/html//p[@class="user-info-other"]/span/text()').extract()
                
                if type(item['liveID']) is list:
                    item['liveID'] = item['liveID'][0] #如果时list则取其一
                item['liveID'] = str(item['liveID']).split('：')[-1]
            except Exception as e:
                print('@get ID error', e, file=sys.stderr)
        
        def getIntroduce(item):
            try:
                item['liveIntroduce'] = response.xpath('/html//p[@class="user-info-description"]/text()').extract()
                
                if type(item['liveIntroduce']) is list:
                    item['liveIntroduce'] = item['liveIntroduce'][0] #如果时list则取其一
                item['liveIntroduce'] = str(item['liveIntroduce'])
            except Exception as e:
                print('@get Introduce error', e, file=sys.stderr)

        def getConstellation(item):
            try:
                data = response.xpath('/html//span[@data-v-7cea7258]/text()').extract()
                #print('##test constellation', item['liveConstellation'])
                for elem in data:
                    if re.match(r'[^\s][^\s]座', elem) is not None:
                        item['liveConstellation'] = elem
                        if type(item['liveConstellation']) is list:
                            item['liveConstellation'] = item['liveConstellation'][0] #如果时list则取其一
                            item['liveConstellation'] = str(item['liveConstellation'])
                    elif re.match(r'快手ID', elem) is not None:
                        print('test', elem, 'is id')
                    else:
                        item['liveLocation'] = elem
                        print('test, location is ', item['liveLocation'])
            except Exception as e:
                print('@get liveConstellation error', e.with_traceback, file=sys.stderr)

        

        def displayItem(item):
            li = ['liveName', 'liveID', 'liveIntroduce', 'liveConstellation']
            print("@@@@item name:", item["liveName"], file=sys.stdout)
            print("@@@@item ID:", item["liveID"], file=sys.stdout)
            print("@@@@item Introduce:", item["liveIntroduce"], file=sys.stdout)
            print("@@@@item Constellation:", item["liveConstellation"], file=sys.stdout)
            print("@@@@item:", item, file=sys.stdout)

        item = KuaishouItem()

        getName(item)
        getID(item)
        getIntroduce(item)
        getConstellation(item)
        displayItem(item)

