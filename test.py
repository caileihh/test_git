# -*- coding: utf-8 -*-
import pandas as pd


def pd_toExcel(data, fileName):  # pandas库储存数据到excel
    ids = []
    rates = []
    length = []
    for i in range(len(data)):
        ids.append(data[i]["id"])
        rates.append(data[i]["rate"])
        # length.append(data[i]["length"])
        # prices.append(data[i]["price"])

    dfData = {  # 用字典设置DataFrame所需数据
        'id':ids,
        '布通率': rates,
        # '线长': length
        # '价格': prices
    }
    df = pd.DataFrame(dfData)  # 创建DataFrame
    df.to_excel(fileName, index=False)  # 存表，去除原始索引列（0,1,2...）


# "-------------数据用例-------------"
# 读取代码
def read(filepath, id):
    fr = open(filepath, 'r')
    dic = {}
    keys = []  # 用来存储读取的顺序
    for line in fr:
        v = line.strip().split(':')
        dic[v[0]] = v[1]
        keys.append(v[0])
    dic["id"] = id
    fr.close()
    print(dic)
    return dic


# # 写入文件代码 通过keys的顺序写入
# fw = open('wdic.txt', 'w')
# for k in keys:
#   fw.write(k + ':' + dic[k] + '\n')
# fw.close()
if __name__ == '__main__':
    testData = []
    for i in range(10100, 10200):
        try:
            filepath = "D:\\Chrome下载\\sample\\16ModuleCase\\16-" + str(i)+"\\judge.txt"
            testData.append(read(filepath, i))
        except Exception as e:
            print(e)

    # testData = [read("score1.txt"), read("judge.txt")]
    fileName = '测试1.xlsx'
    pd_toExcel(testData, fileName)
