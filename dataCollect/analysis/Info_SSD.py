# Info_SSD-v1.1
# 由於需要比較大小的"容量"欄位中只能有數字，否則尋資料庫(filter())時，無法比較大小，所以必須將單位分離出來，儲存在額外的ORM欄位。
import re
from dataCollect.analysis.SpecRefer import brand_refer, trans
import pandas as pd

# SSD：品牌, 介面, 容量

def ssdInfo(store, category, description):

    def ssd(category,description):
        # 品牌(brand)
        brand = "NG"
        for i in brand_refer["ssdLst"]:
            if i == "":
                break
            elif i in str.upper(description):
                brand = i
                break
        for j in brand_refer["ssdLstE"]:
            if brand != "NG" or j == "":
                break
            elif j in str.upper(description):
                brand = trans(j)
                break
    
        # 介面(interface)
        if "SATA3" in str.upper(category):
            interface = "SATA3"
        elif "M.2" in str.upper(category):
            temp = re.findall(r"\d.0",str.upper(category))
            if "PCIE" in str.upper(category) and len(temp) > 0:
                interface = "M.2 PCIe "+temp[0]
            else:
                interface = "NG"
        else:
            interface = "NG"    
    
        # 容量(capacity)
        temp1 = re.findall(r"\d{1,2}TB",str.upper(description))
        temp2 = re.findall(r"\d{1,2}T",str.upper(description))
        temp3 = re.findall(r"\d{3,4}GB",str.upper(description))
        temp4 = re.findall(r"\d{3,4}G",str.upper(description))
        if len(temp1) > 0:
            capacity = temp1[0].strip("TB")
            capUnit = "TB"
        elif len(temp2) > 0:
            capacity = temp2[0].strip("T")
            capUnit = "TB"
        elif len(temp3) > 0:
            capacity = temp3[0].strip("GB")
            capUnit = "GB"
        elif len(temp4) > 0:
            capacity = temp4[0].strip("G")
            capUnit = "GB"
        else:
            capacity = "NG"
            capUnit = "NG"
    
        return brand, interface, capacity, capUnit

    if store == "coolpc":
        brand, interface, capacity, capUnit = ssd(category,description)
    elif store == "newton":
        brand, interface, capacity, capUnit = ssd(category,description)

    return brand, interface, capacity, capUnit


if __name__ == "__main__":
    
    #################### 測試資料 ####################
    data = pd.read_csv("nt-.csv",delimiter=",",encoding="ANSI")
    data1 = data[data["類別"] == "固態硬碟 SSD"]["子類別"]
    data2 = data[data["類別"] == "固態硬碟 SSD"]["品名"]
    ##################################################

    k = 0
    for index, (i,j) in enumerate(zip(data1,data2),start=1):
        brand, interface, capacity, capUnit = ssdInfo("coolpc", i,j)
        if brand == "NG" or interface == "NG" or capacity == "NG" or capUnit == "NG":
            continue
        print(brand,end=" \\ ")
        print(interface,end=" \\ ")
        print(capacity+capUnit,end=" \\ ")
        # print(socket,end=" \\ ")
        # print(size,end=" \\ ")
        k += 1
        print(k)