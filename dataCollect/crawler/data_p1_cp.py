# 2024.12.25 原價屋爬蟲-3.0
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import pandas as pd
import re
from datetime import datetime

print("----- Importing data_p1_cp.py ")

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 無頭模式
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_service = Service(os.environ.get("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver

def cateDescide(cateStr):
    cateSet = {"CPU":"處理器 CPU","MB":"主機板 MB","RAM":"記憶體 RAM","VGA":"顯示卡 Video",
               "SSD":"固態硬碟 SSD","HDD":"硬碟 HDD","CASE":"機殼 CASE","電源供應器":"電源供應器 POWER","散熱器":"CPU空冷散熱器"}
    category_name = "none" # 先預設為 none，也就是不屬於上面字典裡的類別，下面 for 如果有比對到，就會被正確的類別取代，否則就不是我要的類別
    for i in cateSet:
        if str.upper(i) in cateStr:
            category_name = cateSet[i] # 如果有比對到，就用比對到的類別取代 "none"，類別就不是 none
    return category_name

def priceCollect(itemStr,monryMarkNum):
    if monryMarkNum == 0:
        price = -1
        orgPrice = None
        discntend = None
    elif "下殺到" in itemStr and "↘" in itemStr and monryMarkNum > 1:
        prcs = re.findall(r"\$\d+",itemStr)
        price = prcs[-1].lstrip("$") # 取售價
        orgPrice = prcs[-2].lstrip("$") # 取原價錢
        temp = re.findall(r"下殺到.+\d{1,2}\/\d{1,2}",itemStr) # 取折扣期限
        end_date_split = re.findall(r"\d{1,2}\/\d{1,2}",temp[0])[0].split("/") # 取得 temp 中的 "月/日"，同時分開成為 "月" 及 "日"
        if datetime.now().month <= eval(end_date_split[0]): # 決定年，若今天是12月，折扣期限是1月，那麼折扣期限的年就是隔年
            yr = str(datetime.now().year)
        else:
            yr = str(datetime.now().year+1)
        end_date_str = yr+"-"+end_date_split[0]+"-"+end_date_split[1]
        temp = datetime.strptime(end_date_str, "%Y-%m-%d") # 先把日期字串轉成日期型態，就是把 2024-5-11(月、日有時是1位數) 這樣的字串轉成日期型態
        discntend = datetime.strftime(temp, "%Y-%m-%d") # 再把日期型態轉成字串型態，因為 ORM Model 只接受 2024-05-11 月、日 都要是兩位數，這樣轉回來就是2位數
    else: # 不管 $ 有幾個，只要不符合上面兩組條件，$ 一定有至少1個，這時只取最後一個價錢
        prcs = re.findall(r"\$\d+",itemStr)
        price = prcs[-1].lstrip("$") # 取售價
        orgPrice = None # 沒有原價錢
        discntend = None # 沒有折扣期限
    return price, orgPrice, discntend


def coolpc():
    
    url_CP = "https://www.coolpc.com.tw/evaluate.php"
    driver = setup_driver()
    driver.maximize_window()
    ############################################ 會員登入 ############################################
    driver.get(url_CP)
    
    r = driver.page_source
    soop = BeautifulSoup(r, "html.parser")
    
    store = []
    categories = []
    subCate = []
    items = []
    orgPrice = []
    saleEnd = []
    prices = []
    
    print("----- Start crawling coolpc ")

    # 抓取整個選單區塊的 raw data
    menus = soop.select("#tbdy tr") # raw data，每一筆是一個類別的所有資料
    # 對整個選單區塊中的每一個類別，一個一個抽取作處理
    for i in menus: # 每一筆是一個類別的所有資料，也就是每一筆是一個 tr 裡面的所有資料
    
        if i.select("td.t"): # 萬一有哪個 tr 中不存在 class == t 的，就跳過不處理
            cateStr = i.select("td.t")[0].text # 這個類別的名稱，例如 "處理器 CPU"、"主機板 MB"
            cateNames = cateDescide(cateStr) # 判定是不是我要的類別，並統一類別命名方式
            if cateNames == "none":
                continue
        else:
            continue
        
        optGroup = i.select("optgroup") # 這個(大)類別選單中的 raw data，每一筆資料是選單中的一個子類別(標籤=optgroup)
        for j in optGroup:
            
            optgrpName = j.get("label") # 子類別的名稱
            subOptions = j.select("option") # 這個子類別中所有的品項
            
            for k in subOptions: # 取出每一個品項字串
                if chr(8618) in k.text or chr(10084) in k.text or "套餐" in k.text:  # 剔除包含 ↪ 、套餐 或 ❤ 的行
                    continue
                else:
                    k = k.text
                    store.append("原價屋")
                    categories.append(cateNames)
                    subCate.append(optgrpName)
                    monryMarkNum = k.count("$")
                    try:
                        pr, oPr, enddate = priceCollect(k,monryMarkNum) # 售價金額
                        orgPrice.append(oPr)
                        saleEnd.append(enddate)                        
                        if str.isdigit(pr):
                            items.append(k)
                            prices.append(eval(pr))
                        else:
                            items.append(k)
                            prices.append(pr)
                            print(f"ERROR：{cateNames} // {optgrpName}")
                            print(k.text)
                            print("price=",pr)
                    except:
                        prices.append("售價店洽") # 售價
    
    driver.quit()
    chart = pd.DataFrame({"store":store,"category":categories,"sub_cate":subCate,"description":items, "orgPrice":orgPrice, "saleEnd":saleEnd, "price":prices})
    return chart

if __name__ == "__main__":
    chart = coolpc()
    chart.to_csv("z:\\cp.csv",encoding="utf-8-sig")