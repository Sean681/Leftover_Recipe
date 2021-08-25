import google_trans_new
import pandas as pd
import concurrent.futures
import csv

translator = google_trans_new.google_translator(timeout=5)

# 輸入FDA資料
fda_path = "../csv/fda_cleaning.csv"
# FDA資料 to DataFrame
fda_df = pd.read_csv(fda_path)
# FDA全樣品英文名稱
fdaEng = list()

fda_index = list(fda_df.index)

def GoFDA(inputs):
    output = translator.translate(fda_df.loc[inputs]["樣品名稱"], "en", "zh")
    # 加入index(以便日後對應原資料)與英文樣品名稱
    fdaEng.append([inputs, output])

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(GoFDA, fda_index)

# 將輸出儲存為csv
filename = "FDAtoEng.csv"
columns = ['index', 'Eng_name']
with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(columns)
    for data in fdaEng:
        writer.writerow(data)