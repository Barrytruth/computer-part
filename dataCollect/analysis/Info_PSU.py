# Info_PSU-v1.1
# 由於需要比較大小的"瓦數"欄位中只能有數字，否則尋資料庫(filter())時，無法比較大小，所以必須將單位分離出來，儲存在額外的ORM欄位。
import re
from dataCollect.analysis.SpecRefer import brand_refer, trans, correct
import pandas as pd

# 機殼：品牌(brand), 瓦數(walt), 效率等級(grade), 模組化(modular)、靜音(silence)

def psuInfo(store, category, description):

    def psu(category,description):
    
        # 品牌
        brand = "NG"
        brand_C = "NG"
        brand_E = "NG"
        category = correct(category)
        description = correct(description)
        for i,j in zip(brand_refer["psuLst"],brand_refer["psuLstE"]):
    
            check_cate = str.upper(i) not in str.upper(category) and str.upper(j) not in str.upper(category) # 檢查子類別，剃除特價活動等部份
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
    
        # 瓦數(walt)
        # 1. 取得瓦數各段字串
        w_string_W = re.findall(r"\d{3,4}[wW]",str.upper(description)) # 尋找是否有以"W"為尾碼，標示瓦數的字串
        w_string_X = re.findall(r"\d{3,4}[A-Z]",str.upper(description)) # 若找不到W尾碼的，尋找是否有以其他字母為尾碼的 "數字+尾碼" 的字串
        sizeCheck = "SFX" not in str.upper(description)
        if len(w_string_W) > 0 and sizeCheck:
            w_number = re.findall(r"\d{3,4}",w_string_W[0])[0]
            walt = w_number
        elif len(w_string_X) > 0 and sizeCheck:
            w_number = re.findall(r"\d{3,4}",w_string_X[0])[0]
            walt = w_number
        else:
            walt = "NG"
        waltUnit = "W"
    
        # 效率等級(grade)
        if "鈦金" in str.upper(description):
            grade = "鈦金"
        elif "白金" in str.upper(description):
            grade = "白金"
        elif "金牌" in str.upper(description):
            grade = "金牌"
        elif "銀牌" in str.upper(description):
            grade = "銀牌"
        elif "銅牌" in str.upper(description):
            grade = "銅牌"
        else:
            grade = "-無認證-"
            
        # 模組化(modular)
        if "全模" in str.upper(description):
            modular = "全模"
        elif "半模" in str.upper(description):
            modular = "半模"
        else:
            modular = "直出線"
    
    
        # 靜音(silence)
        if "靜音" in str.upper(description):
            silence = "靜音"
        else:
            silence = "無靜音"
    
        return brand, walt, waltUnit, grade, modular, silence

    if store == "coolpc":
        brand, walt, waltUnit, grade, modular, silence = psu(category,description)
    elif store == "newton":
        brand, walt, waltUnit, grade, modular, silence = psu(category,description)

    return brand, walt, waltUnit, grade, modular, silence


if __name__ == "__main__":

    #################### 測試資料 ####################
    data = pd.read_csv("cp-.csv",delimiter=",",encoding="ANSI")
    data1 = data[data["類別"] == "電源供應器 POWER"]["子類別"]
    data2 = data[data["類別"] == "電源供應器 POWER"]["品名"]
    ##################################################

    k = 0
    for i,j in zip(data1,data2):
        brand, walt, waltUnit, grade, modular, silence = psuInfo("coolpc",i,j)
        if brand == "NG" or walt == "NG" or waltUnit == "NG" or grade == "NG" or modular == "NG" or silence == "NG":
            continue
        print(brand,end=" \\ ")
        print(walt+waltUnit,end=" \\ ")
        print(grade,end=" \\ ")
        print(modular,end=" \\ ")
        print(silence,end=" \\ ")
        k += 1
        print(k)