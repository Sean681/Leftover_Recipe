import requests
from bs4 import BeautifulSoup
import csv

csv_path = "./fda.csv"
url = "https://consumer.fda.gov.tw//Food/TFND.aspx?nodeID=178&p="

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}

ss = requests.session()


datas = list()

for p in range(1, 213 + 1):
    print("page {}".format(p))

    res = ss.get(url + str(p), headers=headers)  # Get in main page

    soup = BeautifulSoup(res.text, "html.parser")

    for i in soup.select('td[class="txt_L shortStyleAuto"] a'):

        urlArticle = "https://consumer.fda.gov.tw/Food/" + i["href"]

        resArticle = ss.get(urlArticle, headers=headers)  # Get in article page
        soupArticle = BeautifulSoup(resArticle.text, "html.parser")

        foodName = soupArticle.select('span[id="ctl00_content_lbFoodName"]')[0].text  # Food name
        columns = list()
        data = list()
        columns.append("樣品名稱")
        data.append(foodName)

        for i in soupArticle.select('table[class="rwd-table"] tr')[1:]:

            column = i.select('td[data-th="分析項"]')[0].text
            columns.append(column)

        for i in soupArticle.select('table[class="rwd-table"] tr')[1:]:
                data.append((i.select('td[data-th="每100克含量"]')[0].text).replace(" ", ""))
        datas.append(data)

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(columns)
    for data in datas:
        writer.writerow(data)