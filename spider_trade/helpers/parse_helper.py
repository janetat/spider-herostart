""" 这些方法只适用于详情页, 兼容性和广泛性不强，因为字段结构不同。有些结构字段要css selector，有些需要xpath，有些需要regex """

import re

def get_detail_by_name(name, response):
    """ 根据名字爬取信息

    :param name: 要爬取的字段的名字， 例如公司档案里的字段
    :param response: 返回的是<class 'scrapy.http.response.html.HtmlResponse'> -> TextResponse -> Response
    :return: <class 'str'>
    """
    field = response.xpath(
        "//td[contains(text(),'{name}')]/following-sibling::td/text()".format(name=name)).extract_first()
    return field

def get_detail_by_pattern(pattern, html):
    """ 根据正则爬取信息

    :param pattern: regex
    :param html: <class 'str'>
    :return: None or <class 'str'>
    """
    temp = re.search(pattern, html)
    if temp is None:
        return temp
    ret = temp.group(1)
    return ret

def str_to_list(content):
    """ 将产品字段的字符串转换为列表

    :param content: <class 'str'>
    :return: <class 'list'>
    """
    if not isinstance(content, str):
        content = str(content)
    pattern_sub_symbol = re.compile("[、;；\s。]")
    temp = pattern_sub_symbol.sub(' ', content)
    ret = temp.strip().split()
    return ret


def turn_null_to_str(content, replace_str=""):
    """ 将'', [], ()这些空值转换为str

    :param content:
    :param replace_str:  <class 'str'>
    :return:
    """
    if not content or 'None' in content:
        return replace_str
    return content

