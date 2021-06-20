# -*- coding:utf-8 -*-
# 爬虫基本库
from bs4 import BeautifulSoup
import requests
import json
# 随机数库
import random
# 时间库
import time
# 表格库
import csv
# 可以提前以“ab+”的方式打开文件
import codecs
import pctest
import pctest2

agent_list = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
host = 'https://movie.douban.com/'
url = "https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action="
exitlist = []  # 通过保存浏览过的电影id
cur = {  # 用于恢复到本地纪录之后的请求
    "types": [],  # 所有类型
    'id': [],  # 当前正在请求哪个类型下的电影评论
    'num1': 0,  # 当前正在请求所属类型的第几部电影下的评论
    'num2': 0,  # 当前正在请求电影的第几条评论
}
re_max = 1000  # 请求一定次数后触发休眠


# 获取免费代理ip
def getip():
    pctest.get()
    pctest2.get()
    ip_list = pctest.ip_list
    ip_list.extend(pctest2.ip_list)
    return ip_list


ip_list0 = getip()

s = requests.Session()
s.keep_alive = True


# 获取页面内容
def getHTML(url):
    global re_max
    if re_max == 0:
        re_max = 1000
        t = random.choice([600, 900, 1200, 1500, 1800])
        time.sleep(t)  # 每爬取100条评论，休眠一段时间
    ts = [0.5, 0.7, 0.8, 1, random.randint(1, 3)]
    t = random.choice(ts)
    time.sleep(t)  # 每次请求页面前随机休眠一段时间
    ip_list = ip_list0
    proxies = {"http": random.choice(ip_list)}
    head = {'User-Agent': random.choice(agent_list)}
    t_c = 0
    r = s.get(url, headers=head, proxies=proxies)
    r.raise_for_status()  # 检查请求异常进而执行save
    t_c += 1
    if t_c == 100:
        t_c = 0
        ip_list = getip()
        proxies = {"http": random.choice(ip_list)}
    r.encoding = 'utf-8'
    return r.text


# 截取typeid
def gettypes(html):
    if (html == 'failed'):
        return 'failed'
    soup = BeautifulSoup(html, 'html.parser')
    types = soup.find('div', attrs={'class': 'types'})
    types = types.find_all('a')
    for i in range(len(types)):
        types[i] = host + types[i].get('href')
        types[i] = types[i].split('type=')
        types[i] = types[i][1].split('&')[0]
    print('已获取电影类型...')
    return types


# 截取每部电影信息
def getmoviesdata(typeid):
    # soup = BeautifulSoup(html, 'html.parser')
    # pages = soup.find_all('div', attrs={'class': 'movie-list-item playable unwatched'})  # 无效，js动态数据，这里返回空
    # 获取该类型下的所有电影，js动态数据，通过json获取,以下链接返回json数据
    # https://movie.douban.com/j/chart/top_list_count?type=11&interval_id=100%3A90  该链接返回type11:剧情类型下的所有电影数目,主要获取该类型电影数目
    # https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=100&start=0&limit=20 该链接返回该类型下的20部电影基本信息,主要从中提取电影url,修改limit可以返回更多,实测可以一次性返回所有
    # 下面注释部分是请求该榜单下一共有的电影数量
    # sr1 = 'https://movie.douban.com/j/chart/top_list_count?' + \
    #     'type='+str(typeid)+'&interval_id=100' + \
    #     '%3A90'  # 通过修改type来获取不同类型的电影链接
    # html = getHTML(sr1, hd1)
    # data = json.loads(html)
    # total = data['total']
    sr2 = 'https://movie.douban.com/j/chart/top_list?type=' + str(
        typeid
    ) + '&interval_id=100%3A90&action=&start=' + str(
        cur['num1']
    ) + '&limit=200'  # str(total)   # 每个类型只获取前200部电影,从num1到200的 200 - num1 部电影
    html = getHTML(sr2)
    data = json.loads(html)
    # 对部电影核对是否存在于文件中,每个i是一个movie,判断movieid是否处理过
    if typeid not in cur['id']:  # 该榜单没有被访问过，本地没有该榜单电影数据
        with open("movie.csv", "ab+") as file:
            file.write(codecs.BOM_UTF8)  # 第一次打开，这为了防止在Windows下打开CSV文件出现乱码
        file = open('movie.csv', 'a+', encoding='utf-8', newline='')
        writer = csv.writer(file)
        url = []
        for i in data:
            cur['num1'] += 1
            if len(exitlist) and i['id'] in exitlist:
                continue
            exitlist.append(i['id'])
            url.append(i['url'])
            row = [
                i['id'], i['title'], i['types'], i['regions'], i['actors'],
                i['release_date']
            ]
            writer.writerow(row)
        file.close()
    print('tpye:' + typeid + ',该类型电影榜单已访问...')
    cur['num1'] = 0
    return url


def getrating(s):
    if s == '力荐':
        return 5
    if s == '推荐':
        return 4
    if s == '还行':
        return 3
    if s == '较差':
        return 2
    if s == '很差':
        return 1


# 截取评论信息包括用户信息（uid，uname）
def getreview(mv_url):  # 该功能需要请求2次
    global re_max
    s = mv_url.split('/')
    mid = s[len(s) - 2]
    one_page = 20  # 一页最多20条
    get_page = 5  # 爬取前5页
    for i in range(get_page):
        cur_page = '/comments?start=' + str(
            i * one_page) + '&limit=20&status=P&sort=new_score'
        cur_url = mv_url + cur_page
        # 第一次请求获取用户基本信息uid，uname，rating
        html = getHTML(cur_url)
        soup = BeautifulSoup(html, 'html.parser')
        review_user = soup.findAll('span', attrs={'class': 'comment-info'})
        review_mov = soup.findAll('span', attrs={'class': 'short'})
        with open("reviews.csv", "ab+") as file:
            file.write(codecs.BOM_UTF8)  # 第一次打开，这为了防止在Windows下打开CSV文件出现乱码
        file = open('reviews.csv', 'a+', encoding='utf-8', newline='')
        writer = csv.writer(file)
        for j in range(len(review_user)):
            re_max -= 1  # 此处算一次评论爬取
            # 这条评论的用户信息
            user = review_user[j].find("a")
            uid = user.get('href').split('/')
            uid = uid[len(uid) - 2]
            uname = user.string
            temp = review_user[j].findAll('span')
            rating = getrating(temp[1].get("title"))  # 可能没有
            if rating == '':
                rating = 0
            comment = review_mov[j].string
            row = [mid, uid, uname, rating, comment]
            writer.writerow(row)
            cur['num2'] += 1
            print('已获取' + str(cur['num2']) + '条评论...')
        file.close()
    cur['num2'] = 0
    re_max = 100
    print('已获取到一部电影的评论...')


def saveprocess():
    with open('process.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        # types typeid    the num of movie has been requested     the num of the latest movie comment
        row = [cur['types'], cur['id'], cur['num1'], cur['num2']]
        writer.writerow(row)
    file.close()


def loadprocess():
    try:
        with open('process.csv', 'r') as file:
            reader = csv.reader(file)
            # typeid    the num of movie has been requested     the num of the latest movie comment
            if len(list(reader)):
                row = list(reader)[0]
                cur['types'] = row[0]
                cur['id'] = row[1]
                cur['num1'] = row[2]
                cur['num2'] = row[3]
                print(cur)
            file.close()
        # 恢复exitlist
        with open('movie.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                exitlist.append(row['id'])
            file.close()
        return True  # 表示需要恢复
    except (Exception):  # 文件不存在创建文件,避免触发main里面的save
        file = open('process.csv', 'w')
        file.close()
        return False  # 表示第一次运行


if __name__ == '__main__':
    try:
        recovery = loadprocess()
        typeid = []
        mv_url = []
        if recovery:
            typeid = cur['types']  # 本地恢复types
        else:
            typeid = gettypes(getHTML(url))
            cur['types'] = typeid
        for i in typeid:
            if i in cur['id']:  # 本地恢复mv_url,但是本地没有存movieurl，只好跳过不需要的type榜单请求
                continue
            else:
                mv_url = getmoviesdata(i)  # 访问该榜单
                cur['id'].append(i)  # 添加访问记录
            for j in mv_url:
                getreview(j)
        print('all scuessful!')
    except (Exception):
        print('request error: may be 403， ip或账号被ban')
        saveprocess()  # 请求出错时进行保存
