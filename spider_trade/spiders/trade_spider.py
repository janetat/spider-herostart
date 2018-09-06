"""
    @__author__: allen
    @__date__: 2018-8-28 ~ 9-3
    @__mission__: 爬取环球贸易网，http://www.herostart.com/
    @__demand__: 爬取方面，按省展开，爬完每个省的所有城市再爬取下一个省。
    @__note__: 每个页面对应一个parse函数。 页面一共有4层， 即有4个parse函数。 parse -> parse_city -> parse_company_list -> parse_company
"""

import scrapy
import logging
from logging.handlers import RotatingFileHandler
from spider_trade.items import BusinessItem
from spider_trade.helpers.parse_helper import get_detail_by_name, get_detail_by_pattern, str_to_list, turn_null_to_str

# 创建所需数据的数据模型
# item = BusinessItem()

# 日志
logger = logging.getLogger()
handler = RotatingFileHandler('./spider_trade/logs/logfile.log', maxBytes=10 * 1024 * 1024, backupCount=3)
logger.addHandler(handler)


class TradeSpider(scrapy.Spider):
    name = 'trade'

    start_urls = [
        'http://www.herostart.com/'
    ]

    def parse(self, response):
        """ Layer 1: 解析入口页，爬完一个省再爬另外一个省

        :param response: <class 'scrapy.http.response.html.HtmlResponse'>
        :return:  跳转到Layer 2，并传入回调函数去解析
        """
        for city_list in response.css(".bbody ul li"):
            for city in city_list.css("b~span a"):
                if city:
                    yield response.follow(city, self.parse_city)

    def parse_city(self, response):
        """ Layer 2: 解析区域页(城市), 获取各行各业的链接

        :param response: <class 'scrapy.http.response.html.HtmlResponse'>
        :return: 跳转到Layer 3，并传入回调函数去解析
        """

        industry_list = response.css("div.chcat h2~a::attr('href')")

        for company_list in industry_list:
            yield response.follow(company_list, self.parse_company_list)


    def parse_company_list(self, response):
        """ Layer 3: 解析每个行业的公司列表页，注意：有分页；在最后一页点击“下一页”的时候会返回到所属类别的第一页

        :param response: <class 'scrapy.http.response.html.HtmlResponse'>
        :return: 跳转到Layer 4, 并传入回调函数去解析
        """
        for company in response.css("div.list li a::attr('href')"):
            yield response.follow(company, self.parse_company)

        # 递归解析分页
        max_page_num = ''.join(response.xpath("//a[contains(text(),'下一页')]/following-sibling::cite").re('(\d+)页'))
        current_page_num = ''.join(response.css("div.pages > strong").re("\xa0(\d+)"))

        if max_page_num and current_page_num:
            max_page_num = int(max_page_num)
            current_page_num = int(current_page_num)
        else:
            return

        if current_page_num < max_page_num:
            next_page = response.xpath("//a[contains(text(),'下一页')]/@href")[0]
            yield response.follow(next_page, self.parse_company_list)


    def parse_company(self, response):
        """ Layer 4: 解析公司详情页, 爬取所需的字段需要不同的方式(/helpers/parse_helper.py)

        :param response:  <class 'scrapy.http.response.html.HtmlResponse'>
        :return: 所需信息的模型item
        """

        # response.text is response.body.decode(response.encoding)，自动检测编码，然后解编码
        html = response.text
        pattern_contact = "联系人：([\u4e00-\u9fa5]{0,})"
        pattern_phone = "电话：([\d\s-]+)"
        pattern_cell_phone = "手机：([\d-]+)"
        pattern_address = "地址：([\u4e00-\u9fa5 \d\w]{0,})"
        pattern_email = "邮件：(\w+@\w+.com)"

        item = BusinessItem()

        # 获取数据存储到item里
        item['company_name'] = turn_null_to_str(get_detail_by_name('公司名称', response))
        item['company_type'] = turn_null_to_str(get_detail_by_name('公司类型', response))
        item['product'] = turn_null_to_str(str_to_list(get_detail_by_name('销售的产品', response)))
        item['introduction'] = turn_null_to_str(''.join(response.css("div.pd10 ::text").extract()).strip())
        item['address'] = turn_null_to_str(get_detail_by_pattern(pattern_address, html))
        item['contact'] = turn_null_to_str(get_detail_by_pattern(pattern_contact, html))
        item['phone'] = turn_null_to_str(get_detail_by_pattern(pattern_phone, html))
        item['cell_phone'] = turn_null_to_str(get_detail_by_pattern(pattern_cell_phone, html))
        item['email'] = turn_null_to_str(get_detail_by_pattern(pattern_email, html))
        item['website'] = response.url
        item['status_code'] = response.status

        yield item
