

from urllib.error import HTTPError  # HTTPのエラーを抽出
from urllib.error import URLError  # URLのエラーを抽出
from urllib.request import urlopen
from bs4 import BeautifulSoup

import pandas as pd

print("Modules included")


html = urlopen("https://www.kibutu.com/kibutu.php?university=tohoku")
kibutu = BeautifulSoup(html, "html.parser")
print("Data loaded")

search = kibutu.find_all("tr")
search = pd.Series(search)
# print(search)

search_list = []
for a in search:
    if len(a.find_all("td")) == 3 and a.find_all("tr") == []:
        search_list.append(a)

print("DataPreprocess 1 done")

# %%

index = [str(k).split("\n") for k in search_list]
index = pd.DataFrame(index)
del index[0], index[4], index[5]

print("DataPreprocess 2 done")

# %%

# https://note.nkmk.me/python-pandas-dataframe-rename/

name_dic = {1: "リンク", 2: "教科名", 3: "日付"}
index = index.rename(columns=name_dic)

mr = [BeautifulSoup(j, "html.parser").get_text() for j in index["リンク"]]
sub = [BeautifulSoup(m, "html.parser").get_text() for m in index["教科名"]]
timestamp = [BeautifulSoup(n, "html.parser").get_text() for n in index["日付"]]
link = [str(BeautifulSoup(l, "html.parser").a["href"]) for l in index["リンク"]]

index["リンク"] = pd.Series(link)
index["教科名"] = pd.Series(sub)
index["日付"] = pd.Series(timestamp)
index["教官名"] = pd.Series(mr)
print("All preprocesses done")

# %%
while True:
    prompt = int(input("検索方法を半角数字で選択\n1:教官名でサーチ\n2:教科名でサーチ\n\n0:終了　："))
    if prompt == 0:
        break

    key = input("検索キーワードを入力　：")

    area = "教官名" if prompt == 1 else "教科名"

    target = index[index[area].str.contains(key)]

    print(target)

    print(f"You got {len(target)} item(s)\nNow loading contents ...")

    describes = ""
    for links in target["リンク"]:
        des_html = urlopen("https://www.kibutu.com/"+str(links))
        des_soup = BeautifulSoup(des_html, "html.parser")
        table = des_soup.find_all("table")
        describes += table[len(table)-1].get_text() if table != [] else ""
    print(describes)
# %%
# import matplotlib.pyplot as plt

# # del index[index["日付"].str.contains("線形代数")]
# gat = [a[0:4] for a in index["日付"]]
# for b in range(len(gat)):
#     if gat[b] =="線形代数":
#         gat[b]=2003
#     else:
#         gat[b]=int(gat[b])
# index["集計用"] = pd.Series(gat)
# _count = index.groupby("集計用").count()
# _count = _count["リンク"]
# print(_count.describe())
# _count.plot(xticks=range(2003,2019,1),figsize=(5, 5))
# plt.show()
