# 豆瓣电影评论爬虫  
- 通过豆瓣电影分类排行榜页面爬取影片信息，进一步通过每一部电影页面爬取影评信息
- 利用Requests和bs4编写爬虫，建立会话随机初始化User-Agent和代理ip，每爬取500次或出现爬取异常刷新会话。

## 开发环境
- Windows 10 1909
- PyCharm（Community Edition）
- Python 3.7
- 第三方库：
    1. requests：HTTP库，用于网络访问；
    2. beautifulsoup：网页解释库，提供lxml的支持
