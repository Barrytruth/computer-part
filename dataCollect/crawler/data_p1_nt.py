# 2024.12.22 紐頓爬蟲(函式)-2.1
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import re

print("----- Importing data_p1_nt.py ")

def cateDescide(cateStr):
    cateSet = {"CPU":"處理器 CPU","MB":"主機板 MB","RAM":"記憶體 RAM","VGA":"顯示卡 Video",
               "SSD":"固態硬碟 SSD","HDD":"硬碟 HDD","CASE":"機殼 CASE","電源供應器":"電源供應器 POWER","散熱器":"CPU空冷散熱器"}
    category_name = "none" # 先預設為 none，也就是不屬於上面字典裡的類別，下面 for 如果有比對到，就會被正確的類別取代，否則就不是我要的類別
    for i in cateSet:
        if str.upper(i) in cateStr:
            category_name = cateSet[i] # 如果有比對到，就用比對到的類別取代 "none"，類別就不是 none
    return category_name

def priceCollect(itemStr):
    if "價格店洽" in itemStr:
        price = -1
        orgPrice = None
        discntend = None
    elif "限時特價至" in itemStr:
        prcs = re.findall(r"\$\d+",itemStr)
        price = prcs[-1].lstrip("$") # 取售價，取最後一個價錢
        orgPrice = None
        temp = re.findall(r"限時特價至.+\d{4}-\d{1,2}-\d{1,2}",itemStr) # 取折扣期限：字串
        discntend = re.findall(r"\d{4}-\d{1,2}-\d{1,2}$",temp[0])[0] # 取折扣期限：去掉前面字串，取得確實日期
    else: # 取最後一個價錢
        prcs = re.findall(r"\$\d+",itemStr)
        price = prcs[-1].lstrip("$") # 取售價
        orgPrice = None # 沒有原價錢
        discntend = None # 沒有折扣期限
    return price, orgPrice, discntend


def newton():

    url_NT = "https://nt66mobile.com.tw/index.php"
    r = requests.get(url_NT)
    r = r.text
    soop = BeautifulSoup(r, "html.parser")
    
    store = []
    categories = []
    subCate = []
    items = []
    saleEnd = []
    prices = []
    orgPrice = []
    
    print("----- Start crawling newton ")

    # 抓取整個選單區塊的 raw data
    menus = soop.select("div.product-row.product_data") # raw data，每一筆是一個類別的所有資料，也就是每一筆是一個 product-row.product_data 裡面的所有資料
    # 對整個選單區塊中的每一個類別，一個一個抽取作處理
    for i in menus: # 每一筆是一個類別的所有資料
    
        if i.select("div.column_category"): # 萬一有哪個 div 中不存在 class == column_category 的，就跳過不處理
            cateStr = i.select("div.column_category")[0].text # 這個類別的名稱，例如 "處理器 CPU"、"主機板 MB"
            cateNames = cateDescide(cateStr) # 判定是不是我要的類別，並統一類別命名方式
            if cateNames == "none":
                continue
        else:
            continue
    
        optGroup = i.select("optgroup") # 這個(大)類別選單中的 raw data，每一筆資料是選單中的一個子類別(標籤=optgroup)
        for j in optGroup:
    
            optgrpName = j.get("label") # 子類別的名稱
            subOptions = j.select("option") # 這個子類別中所有的品項
            
            for k in subOptions:
                description = k.text.strip().replace("\n","").replace("\t","")
                if k.text.strip().startswith("-") or chr(8618) in k.text or (len(cateNames) == 1 and ord(cateNames) == 32):
                    continue
                else:
                    store.append("紐頓")
                    categories.append(cateNames)
                    subCate.append(optgrpName) 
                    items.append(description)
                    prs, orgprs, discntend = priceCollect(description)
                    orgPrice.append(orgprs)
                    saleEnd.append(discntend)
                    prices.append(prs)
    
    chart = pd.DataFrame({"store":store,"category":categories,"sub_cate":subCate,"description":items, "orgPrice":orgPrice, "saleEnd":saleEnd, "price":prices})
    return chart

if __name__ == "__main__":
    chart = newton()
    chart.to_csv("z:\\nt.csv",encoding="utf-8-sig")