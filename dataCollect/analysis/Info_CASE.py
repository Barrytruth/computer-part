# Info_CASE-v1.0
# 由於目前同樣的 code 對 coolpc 和 newton 都能判斷，所以目前只使用一組程式碼。
import re
from dataCollect.analysis.SpecRefer import brand_refer, trans, correct
import pandas as pd

# 機殼：尺寸, 側板, 靜音

def caseInfo(store, category, description):

    def case(category,description):

        brand = "NG"
        brand_C = "NG"
        brand_E = "NG"
        category = correct(category)
        description = correct(description)
        for i,j in zip(brand_refer["caseLst"],brand_refer["caseLstE"]):

            check_cate = str.upper(i) not in str.upper(category) and str.upper(j) not in str.upper(category) # 檢查子類別，剃除特價活動等部份
            found_cht = (str.upper(j) in str.upper(category)) or (str.upper(j) in str.upper(description)) # 是否搜尋到中文廠牌名稱
            found_eng = (str.upper(j) in str.upper(category)) or (str.upper(j) in str.upper(description)) # 是否搜尋到英文廠牌名稱
            if i == "" and j == "": # 如果搜尋到空值，就代表搜尋完了，因為 "" 是 SpecRefer 中為了使每個串列長度相同的填補值
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
    
        # 尺寸(size)
        size = "NG"
        if len(re.findall(r"ATX",str.upper(description))) > 0:
            if "M-ATX" in str.upper(description):
                size = "M-ATX"
            elif "E-ATX" in str.upper(description):
                size = "M-ATX"
            else:
                size = "ATX"
        elif len(re.findall(r"ITX",str.upper(description))) > 0:
            if "MINI-ITX" in str.upper(description):
                size = "MINI-ATX"
            else:
                size = "ITX"
        elif len(re.findall(r"EEB",str.upper(description))) > 0:
            size = "EEB"
            
        # 側板(gside)
        if "透測" in str.upper(description) or "玻璃" in str.upper(description) or "克力" in str.upper(description):
            gside = "透測"
        else:
            gside = "無透測"
    
    
        # 靜音(silence)
        if "靜音" in str.upper(description):
            silence = "靜音"
        else:
            silence = "無靜音"
    
        return brand, size, gside, silence

    if store == "coolpc":
        brand, size, gside, silence = case(category,description)
    elif store == "newton":
        brand, size, gside, silence = case(category,description)

    return brand, size, gside, silence


if __name__ == "__main__":
    
    #################### 測試資料 ####################
    data = pd.read_csv("cp-.csv",delimiter=",",encoding="ANSI")
    data1 = data[data["類別"] == "機殼 CASE"]["子類別"]
    data2 = data[data["類別"] == "機殼 CASE"]["品名"]
    ##################################################

    k = 0
    for i,j in zip(data1,data2):
        brand, size, gside, silence = caseInfo("coolpc",i,j)
        if brand == "NG" or size == "NG" or gside == "NG" or silence == "NG":
            continue
        print(brand,end=" \\ ")
        print(size,end=" \\ ")
        print(gside,end=" \\ ")
        print(silence,end=" \\ ")
        # print(rpm,end=" \\ ")
        k += 1
        print(k)