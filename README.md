# 爬取[环球贸易网](http://www.herostart.com/)中的[公司黄页](http://www.herostart.com/gongsi/bjzgydzjsyxzrgs.html)
初学Scrapy练手项目2

Based on Scrapy + MongoDB

# Settings
在/helpers/proxy_helper.py里设置PROXIES_URL(例如快代理的API)

# Run
```
    scrapy crawl trade
```

# 出现<u>部分空白</u>的原因是
1. 解析器写得不好，产品那里，有<a>标签的，有纯文本的，有td的。已解决。
2. 有些公司没有提供部分的字段。

# 出现<u>全部空白</u>的条目原因是
1. 解码网页出错。html = response.text.decode('gbk') 有些会页面出错：UnicodeDecodeError: 'gbk' codec can't decode byte 0xbd in position 6837: illegal multibyte sequence。 也即是，网站中有些字符不是gbk编码。要用html = response.text可以解决(same as response.body.decode(response.encoding))。发现某些网站的编码是gbk的超集gb18030
2. 被封IP且没做处理，直接存进MongoDB。

# 代理IP的获取与分配
方法一：直接从url获取ip，每个request(每个页面)单独配一个ip。100个ip就要100个http。 前提是获取代理的url每次返回一个代理ip。只要ip够多，自动忽略封ip机制。
方法二：定时构建代理池（方法挺笨的，用while True + time.sleep），例如获取100个ip，每次只消耗1个http请求，相当于刷新网页一次。然后从代理池随机分配，定时刷新。
方法三：方法二的变种。也是用代理池pool，从代理池用随机分配。如果出现异常（代理失效），pool.delete(ip)。当pool的ip小于一定数量时，再补充。
方法二的核心是定时刷新代理池，是整体ip替换。方法三是部分ip替换。

方法一优点： 速度快，土豪必备，金钱成本高，时间成本低。(HTTP GET请求的消耗可以忽略，因为代理网站响应快)。而且，因为是每一个页面一个单独的ip, 那么就不用delay去爬。)
方法二优点： 定时设置好的话，能最大化利用代理ip。

方法一缺点： Scrapy里面有个CONCURRENT_REQUESTS参数。并发连接数如果很大，并且每个连接配一个代理ip,当很多代理ip失效时，调度器忙着重试，而不是真正去爬取页面。所以性能急剧下降。
方法二缺点： 实际上，并不知道目标网站的封ip的阈值、频率；还有获取的代理ip可能失效；要不断调整刷新代理池的间隔、代理ip的数量。这两个主要因素造成时间成本大。

此处用方法一，因为方法二调参耗费时间太长。对于现在我的水平来说，方法三在scrapy中实现难度大。

# 去重
Scrapy自带去重功能，默认开启。如过设置dont_filter=True则不去重。
原理是通过request_fingerprint函数，对Request对象生成指纹，存在内存的一个set里。
```
from scrapy import dupefilters
```

# 断点重传
核心思想是保存上一次最后的爬取状态。
```
scrapy crawl somespider -s
```
原理是将状态保存在文件里
恢复也是一样的命令：
```
scrapy crawl somespider -s
```
或者在settings.py里配置JOBDIR='./crawls/trade-1'
注意，只需要按一次Ctrl+C，按多一次无法恢复。

# 缺点
1.  没有使用LinkExtractor整站爬取功能。

# 难点
1. 不清楚调度器如何调度。默认任务管理都是Scrapy自动完成的。
scrapy-redis 和 scrapy 有什么区别？ - 杨恒的回答 - 知乎
https://www.zhihu.com/question/32302268/answer/55724369
https://docs.scrapy.org/en/latest/search.html?q=scheduler&check_keywords=yes&area=default#

# Todo
1. 解决全部空白的数据存进MongoDB(用re找出返回的源码是否有"404，访问太快")这些字眼；如果有，则不yield data，不存进MongoDB中

