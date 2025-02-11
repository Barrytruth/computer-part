# Info_HeatSink-v1.1
# 由於需要比較大小的"高度"欄位中只能有數字，否則尋資料庫(filter())時，無法比較大小，所以必須將單位分離出來，儲存在額外的ORM欄位。

import re
from dataCollect.analysis.SpecRefer import brand_refer, trans, correct
import pandas as pd

    # 機殼：品牌(brand), 高度(height), 導管(pipe), 方向(direct)

def heatsinkInfo(store, category, description):

    def heatsink(category,description):
    
        # 品牌
        brand = "NG"
        brand_C = "NG"
        brand_E = "NG"
        category = correct(category)
        description = correct(description)
        for i,j in zip(brand_refer["heatsinkLst"],brand_refer["heatsinkLstE"]):
    
            check_cate = str.upper(i) not in str.upper(category) and str.upper(j) not in str.upper(category) or ("厚" in description)# 檢查子類別，剃除特價活動等部份，同時排除水冷
            found_cht = (str.upper(i) in str.upper(category)) or (str.upper(i) in str.upper(description)) # 是否搜尋到中文廠牌名稱
            found_eng = (str.upper(j) in str.upper(category)) or (str.upper(j) in str.upper(description)) # 是否搜尋到英文廠牌名稱
            if i == "" and j == "": # 如果搜尋到空值，就代表已經搜尋到最後，就是搜尋完了，因為 "" 是 SpecRefer 中為了使每個串列長度相同的填補值
                break
            elif found_cht == False and found_eng == True: # 若只搜尋到英文名稱，就以翻譯方式得到中文名稱
                if check_cate:
                    break
                brand_E = j
                brand_C = trans(j)
                brand = brand_C + "：" + brand_E
                break
            elif found_cht == True and found_eng == False: # 若只搜尋到中文名稱，就以翻譯方式得到英文名稱
                if check_cate:
                    break
                brand_E = trans(i)
                brand_C = i
                brand = brand_C + "：" + brand_E
                break
            elif found_cht == True and found_eng == True: # 若中英文名稱都搜尋到，就直接結合
                if check_cate:
                    break
                brand_E = j
                brand_C = i
                if brand_C == brand_E:
                    brand = brand_C
                else:
                    brand = brand_C + "：" + brand_E
                break
    
        # 高度(height)
        temp1 = re.findall(r"高度\d{1,2}\.?\d{,2}",str.upper(description))
        temp2 = re.findall(r"高\d{1,2}\.?\d{,2}",str.upper(description))
        temp3 = re.findall(r"\d{1,2}\.?\d{,2}CM",str.upper(description))
        temp4 = re.findall(r"\d{1,2}\.\d{1,2}",str.upper(description))
        if len(temp1) > 0:
             height = re.findall(r"\d{1,2}\.?\d{,2}",temp1[0])[0]
        elif len(temp2) > 0:
            height = re.findall(r"\d{1,2}\.?\d{,2}",temp2[0])[0]
        elif len(temp3) > 0:
            height = re.findall(r"\d{1,2}\.?\d{,2}",temp3[0])[0]
        elif len(temp4) > 0:
            height = re.findall(r"\d{1,2}\.?\d{,2}",temp4[0])[0]
        else:
            height = "NG"
        hUnit = "cm"
    
        # 導管(pipe)
        temp1 = re.findall(r"\d導管",str.upper(description))
        temp2 = re.findall(r"導管\*\d",str.upper(description))
        temp3 = re.findall(r"\d熱導管",str.upper(description))
        temp4 = re.findall(r"熱管\*\d",str.upper(description))
        if len(temp1) > 0:
            pipe = re.findall(r"\d",temp1[0])[0]+"導管"
        elif len(temp2) > 0:
            pipe = re.findall(r"\d",temp2[0])[0]+"導管"
        elif len(temp3) > 0:
            pipe = re.findall(r"\d",temp3[0])[0]+"導管"
        elif len(temp4) > 0:
            pipe = re.findall(r"\d",temp4[0])[0]+"導管"
        else:
            pipe = "無資料"
        
        # 方向(direct)
        if "下吹" in str.upper(description):
            direct = "下吹式"
        else:
            direct = "塔式"
    
        return brand, height, hUnit, pipe, direct

    if store == "coolpc":
        brand, height, hUnit, pipe, direct = heatsink(category,description)
    elif store == "newton":
        brand, height, hUnit, pipe, direct = heatsink(category,description)

    return brand, height, hUnit, pipe, direct

if __name__ == "__main__":
    
    #################### 測試資料 ####################
    data = pd.read_csv("cp-.csv",delimiter=",",encoding="ANSI")
    data1 = data[data["類別"] == "CPU空冷散熱器"]["子類別"]
    data2 = data[data["類別"] == "CPU空冷散熱器"]["品名"]
    ##################################################
    
    k = 0
    for i,j in zip(data1,data2):
        brand, height, hUnit, pipe, direct = heatsinkInfo("coolpc",i,j)
        if brand == "NG" or height == "NG" or hUnit == "NG" or pipe == "NG" or direct == "NG":
            continue
        print(brand,end=" \ ")
        print(height+hUnit,end=" \ ")
        print(pipe,end=" \ ")
        print(direct,end=" \ ")
        # print(silence,end=" \ ")
        k += 1
        print(k)
        # if k == 120:
        #     print("debug")