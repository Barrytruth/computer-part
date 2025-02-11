# Info_HDD-v1.1
# 由於5400轉的硬碟轉速資料混亂，5640轉的只有2個，其他不知是不是原價屋或紐頓打錯字，
# 會使得轉速除了5400和7200多了好幾個選項，選單太亂，因此修改資料組成方式，改成只有5400和7200兩種
# 由於需要比較大小的"容量"欄位中只能有數字，否則尋資料庫(filter())時，無法比較大小，所以必須將單位分離出來，儲存在額外的ORM欄位。

import re
from dataCollect.analysis.SpecRefer import brand_refer, trans
import pandas as pd

# HDD：品牌, 尺寸, 容量, 轉速

def hddInfo(store, category, description):

    def hdd(category,description):
        #  品牌(brand)
        brand = "NG"
        for i in brand_refer["hdLst"]:
            if i == "":
                break
            elif str.upper(i) in str.upper(description):
                brand = i
                break
        for j in brand_refer["hdLstE"]:
            a = str.upper(j)
            if brand != "NG" or j == "":
                break
            elif a in str.upper(description):
                brand = trans(j)
                break

        # 尺寸(size)
        if "2.5" in str.upper(category):
            size = "2.5吋"
        elif "3.5" in str.upper(category):
            size = "3.5吋"
        else:
            size = "NG"
    
        # 用途(use)
        if "監控" in str.upper(category):
            use = "監控碟"
        elif "企業" in str.upper(category):
            use = "企業碟"
        elif "NAS" in str.upper(category):
            use = "NAS碟"
        else:
            use = "傳統碟"
    
        # 容量(capacity)
        temp1 = re.findall(r"\d{1,2}TB",str.upper(description))
        temp2 = re.findall(r"\d{1,2}T",str.upper(description))
        temp3 = re.findall(r"\d{3}GB",str.upper(description))
        if len(temp1) > 0:
            capacity = temp1[0].strip("TB")
            capUnit = "TB"
        elif len(temp2) > 0:
            capacity = temp2[0].strip("T")
            capUnit = "TB"
        elif len(temp3) > 0:
            capacity = temp3[0].strip("GB")
            capUnit = "GB"
        else:
            capacity = "NG"
    
    
        # 轉速(rpm)
        temp = re.findall(r"\d{4,5}轉",str.upper(description))
        if len(temp) > 0:
            if eval(temp[0].strip("轉")) < 6000:
                rpm = "5400轉"
            elif eval(temp[0].strip("轉")) >= 7000:
                rpm = "7200轉"
        else:
            rpm = "NG"

        return brand, size, use, capacity, capUnit, rpm

    if store == "coolpc":
        brand, size, use, capacity, capUnit, rpm = hdd(category,description)
    elif store == "newton":
        brand, size, use, capacity, capUnit, rpm = hdd(category,description)

    return brand, size, use, capacity, capUnit, rpm

if __name__ == "__main__":
    
    #################### 測試資料 ####################
    data = pd.read_csv("cp-.csv",delimiter=",",encoding="ANSI")
    data1 = data[data["類別"] == "硬碟 HDD"]["子類別"]
    data2 = data[data["類別"] == "硬碟 HDD"]["品名"]
    ##################################################

    k = 0
    for i,j in zip(data1,data2):
        brand, size, use, capacity, capUnit, rpm = hddInfo("coolpc", i,j)
        if brand == "NG" or size == "NG" or use == "NG" or capacity == "NG" or capUnit == "NG" or rpm == "NG":
            continue
        print(brand,end=" \ ")
        print(size,end=" \ ")
        print(use,end=" \ ")
        print(capacity+capUnit,end=" \ ")
        print(rpm,end=" \ ")
        k += 1
        print(k)