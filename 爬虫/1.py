# 用来爬取京东商品评论
import json
import re
from urllib import request
import time
from selenium import webdriver
from bs4 import BeautifulSoup

header_dict = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
}


def get_http(load_url, header=None):
    res = ""
    try:
        # req = request.Request(url=load_url, headers=header)  # 创建请求对象
        # coonect = request.urlopen(req)  # 打开该请求
        # byte_res = coonect.read()  # 读取所有数据，很暴力
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--dns-prefetch-disable')
        options.add_argument('--no-referrers')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-audio')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument("--window-size=4000,1600")
        chrome = webdriver.Chrome(options=options)
        chrome.get(load_url)
        html=chrome.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # [s.extract() for s in soup("script")]
        # ss = soup.select('pre')[0]
        # res = json.loads(ss.text)
        res=soup.select("html body")
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', html)
        res=dd
        # print(res)


        # try:
        #     res = byte_res.decode(encoding='utf-8')
        # except:
        #     try:
        #         res = byte_res.decode(encoding='gbk')
        #     except:
        #         res = ""
    except Exception as e:
        print(e)
    return res


pid = "100014352501"  # 页面上的产品id
fout = open("./" + pid + ".csv", "w", encoding='utf-8')  # 输出文件
fout.write("uid,nickname,time,star,comment\n")  # 写csv头
for score in ["3", "2", "1"]:  # 爬取好中差评3好评，2中评，1差评，0默认评论
    # 这个链接和从网页上的链接不太一样，少了几个参数，加载出来的是json数据。
    url0 = "https://sclub.jd.com/comment/productPageComments.action?productId=" + pid + "&score=" + score + "&sortType=6&page="
    # 调整页码，这里只爬取前5页
    for page in range(5):
        print(page)
        url = url0 + str(page) + "&pageSize=10&isShadowSku=0&rid=0&fold=1"
        res = get_http(url, header_dict)
        time.sleep(1)
        if res == None or len(res) <= 30:
            print("加载错误", url)
            continue
        jobj = json.loads(res)  # 解析json

        comments = jobj["comments"]
        if len(comments) == 0:
            break
        # 提取每一页的评论数据并保存
        for comment in comments:
            userImage = comment["userImage"]
            nickname = comment["nickname"]
            uid = str(hash(userImage + nickname))[0:18]
            content = comment["content"]
            creationTime = comment["creationTime"]
            score1 = str(comment["score"])
            fout.write(uid + "," + nickname + "," + creationTime + "," + score1 + "," + content + "\n")
fout.close()
