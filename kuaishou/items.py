# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 要求的信息
# 通过主播的名字找到以下信息

# 主播的名字 头像 各种id 名字下的介绍 性别 星座 城市 粉丝数 关注数 作品量
# 每个作品中的点赞数 播放量 发布时间
# 作品评论中的 评论人 评论内容 评论时间

# 最后将数据放到mysql中

class KuaishouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #profile
    liveName = scrapy.Field() #主播名
    livePhoto = scrapy.Field()#主播照片
    liveID = scrapy.Field() #主播id
    liveIntroduce = scrapy.Field() #简介
    liveSex = scrapy.Field() #性别
    liveConstellation = scrapy.Field() #星座
    liveLocation = scrapy.Field() #地区

    liveFans = scrapy.Field() #粉丝数
    liveFollows = scrapy.Field() #关注数
    liveProductions = scrapy.Field() #作品数
    liveProductionList = scrapy.Field() #作品详情
    pass


class commentItem(scrapy.Item):
    commentList = scrapy.Field  #评论列表， 用列表记录
    productLink = scrapy.Field  #作品的url
    # name = scrapy.Field() #评论人名
    # content = scrapy.Field() #评论内容
    # time = scrapy.Field() #评论时间
    # like = scrapy.Field() #喜欢的人数
    # replyTo = scrapy.Field() #回复对象
    # subcomment = scrapy.Field() #子评论

