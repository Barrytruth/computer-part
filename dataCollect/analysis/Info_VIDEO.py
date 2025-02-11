# Info_VIDEO-v1.1
# 由於需要比較大小的"長度"和"GDDR"中只能有數字，否則尋資料庫(filter())時，無法比較大小，所以必須將單位分離出來，儲存在額外的ORM欄位。
import re
from dataCollect.analysis.SpecRefer import brand_refer, trans
import pandas as pd

# Video：品牌、陣營、顯示晶片、長度、顯示記憶體

def videoInfo(store, category, description):

    def video(category,description):
        #  品牌(brand)
        brand = "NG"
        for i in brand_refer["videoLst"]:
            if i == "":
                break
            elif i in str.upper(description):
                brand = i
                break
        for j in brand_refer["videoLstE"]:
            if brand != "NG" or j == "":
                break
            elif j in str.upper(description):
                brand = trans(j)
                break
    
        # 陣營(camp)
        if "NVIDIA" in str.upper(category):
            camp = "NVIDIA"
        elif "AMD" in str.upper(category):
            camp = "AMD"
        else:
            camp = "NG"
    
        # 顯示晶片(vchip)
        if camp == "NVIDIA":
            temp1 = re.findall(r"NVIDIA.RTX.?\d{4}",str.upper(category))
            temp2 = re.findall(r"NVIDIA.GT.?\d{3,4}",str.upper(category))
            if len(temp1) > 0:
                vchip = re.findall(r"RTX.?\d{4}",temp1[0])[0]
                vchip = re.sub(r"[^a-zA-Z0-9]","",vchip) + ("Ti" if "TI" in str.upper(category) else "") + (" SUPER" if "SUPER" in str.upper(category) else "")
            elif len(temp2) > 0:
                vchip = re.findall(r"GT.?\d{3,4}",temp2[0])[0]
                vchip = re.sub(r"[^a-zA-Z0-9]","",vchip) + ("Ti" if "TI" in str.upper(category) else "") + (" SUPER" if "SUPER" in str.upper(category) else "")
            else:
                vchip = "NG"
        elif camp == "AMD":
            temp = re.findall(r"AMD RADEON RX\d{4}",str.upper(category))
            if len(temp) > 0:
                vchip = re.findall(r"RX.?\d{4}",temp[0])[0]
                vchip = re.sub(r"[^a-zA-Z0-9]","",vchip)
            else:
                vchip = "NG"
        else:
            vchip = "NG"
    
        # 長度(length)
        temp = re.findall(r"\d{2}\.?\d{,2}CM",str.upper(description))
        if len(temp) > 0:
            length = temp[0].strip("CM")
        else:
            length = "NG"
        lenUnit = "cm"
    
        
        # 顯示記憶體(gddr)
        temp1 = re.findall(r"\d{1,3}GB",str.upper(category)) # 小分類有GB的
        temp2 = re.findall(r"\d{1,3}G",str.upper(category)) # 小分類有G的
        temp3 = re.findall(r"\d{1,3}GB",str.upper(description)) # 產品敘述有GB的
        temp4 = re.findall(r"\d{1,3}G",str.upper(description)) # 產品敘述有G的
        if len(temp1) > 0:
            gddr = temp1[0].split("G")[0]
        elif len(temp2) > 0:
            gddr = temp2[0].split("G")[0]
        elif len(temp3) > 0:
            gddr = temp3[0].split("G")[0]
        elif len(temp4) > 0:
            gddr = temp4[0].split("G")[0]
        else:
            gddr = "NG"
        gddrUnit = "GB"
    
        return brand, camp, vchip, length, lenUnit, gddr, gddrUnit

    if store == "coolpc":
        brand, camp, vchip, length, lenUnit, gddr, gddrUnit = video(category,description)
    elif store == "newton":
        brand, camp, vchip, length, lenUnit, gddr, gddrUnit = video(category,description)

    return brand, camp, vchip, length, lenUnit, gddr, gddrUnit


if __name__ == "__main__":
    
    #################### 測試資料 ####################
    data = pd.read_csv("nt-.csv",delimiter=",",encoding="ANSI")
    data1 = data[data["類別"] == "顯示卡 Video"]["子類別"]
    data2 = data[data["類別"] == "顯示卡 Video"]["品名"]
    ##################################################

    k = 0
    for i,j in zip(data1,data2):
        brand, camp, vchip, length, lenUnit, gddr, gddrUnit = videoInfo("newton", i,j)
        if brand == "NG" or camp == "NG" or vchip == "NG" or length == "NG" or lenUnit == "NG" or gddr == "NG" or gddrUnit == "NG":
            continue
        if vchip == "RTX4080 SUPER":
            print("debug",end="---")
        print(brand,end=" \ ")
        print(camp,end=" \ ")
        print(vchip,end=" \ ")
        print(length+lenUnit,end=" \ ")
        print(gddr+gddrUnit,end=" \ ")
        k += 1
        print(k)