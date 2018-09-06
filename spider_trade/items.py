# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BusinessItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 公司名称
    company_name = scrapy.Field()
    # 公司类型
    company_type = scrapy.Field()
    # 简介
    introduction = scrapy.Field()
    # 产品
    product = scrapy.Field()
    # 联系人
    contact = scrapy.Field()
    # 电话
    phone = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 邮件
    email = scrapy.Field()
    # 手机
    cell_phone = scrapy.Field()
    # 网址
    website = scrapy.Field()
    # 状态码
    status_code = scrapy.Field()

