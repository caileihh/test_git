import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('爬虫/100012015170.csv', error_bad_lines=False)['star']
star = []
for level in data:
    if level == 5:
        star.append("好")
    elif level == 4:
        star.append("良好")
    elif level == 3:
        star.append("中")
    elif level == 2:
        star.append("差")
    elif level == 1:
        star.append("极差")
    # else:
    #     star.append(0)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(12, 8))
plt.hist(star, bins=17)
plt.xlabel('评价等级（依次为5星~1星评论）', size=18)
plt.ylabel('人数', size=20)
plt.savefig('评分.jpg')
