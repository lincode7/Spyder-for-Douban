from bs4 import BeautifulSoup
import requests
import random


ip_list = []


def get():
    x = random.choice(range(1, 10))
    url = "http://www.66ip.cn/"+str(x)+".html"
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    r = requests.get(url, headers=head)
    print("状态", r.status_code)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')
    h = soup.findAll('div', attrs={'class': 'containerbox boxindex'})
    h1 = h[0].findAll('tr')
    for j in range(len(h1) - 1):
        td = h1[j + 1].findAll('td')
        ip = "http://"+td[0].string.replace(" ", "")+":"+td[1].string.replace(" ", "")
        ip_list.append(ip)

