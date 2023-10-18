import requests
from bs4 import BeautifulSoup
from pyecharts.charts import Bar
from pyecharts import options as opts

ALL_data = []


def parse_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.132 Safari/537.36"}
    response = requests.get(url, headers=headers)
    text = response.content.decode("utf-8")
    soup = BeautifulSoup(text, 'html5lib')  # html5lib容错性很强
    divs = soup.find("div", class_="conMidtab")
    tables = divs.find_all("table")
    # print(tables)
    for table in tables:
        trs = table.find_all("tr")[2:]
        for index, tr in enumerate(trs):
            tds = tr.find_all("td")
            if index == 0:
                city_name = tds[1]
                city = list(city_name.stripped_strings)[0]
            else:
                city_name = tds[0]
                city = list(city_name.stripped_strings)[0]
                temp = tds[-2]
                min_temp = list(temp.stripped_strings)[0]
                ALL_data.append({'city': city, 'min_temp': int(min_temp)})


def main():
    urls = ["http://www.weather.com.cn/textFC/gat.shtml#",
            "http://www.weather.com.cn/textFC/hb.shtml#",
            "http://www.weather.com.cn/textFC/db.shtml#"]
    for url in urls:
        parse_url(url)
    ALL_data.sort(key=lambda data: data['min_temp'])
    data = ALL_data[0:10]
    cities = list(map(lambda x: x['city'], data))
    temps = list(map(lambda x: x['min_temp'], data))
    bar = (
        Bar().add_xaxis(cities).add_yaxis('', temps).set_global_opts(title_opts=opts.TitleOpts(title="中国天气最低气温排行"))
    )
    bar.render("weather.html")


main()
