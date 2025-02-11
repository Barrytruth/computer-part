# Info_RAM-v1.1
# 由於需要比較大小的"容量"欄位中只能有數字，否則尋資料庫(filter())時，無法比較大小，所以必須將單位分離出來，儲存在額外的ORM欄位。
# RAM：品牌、架構、通道數、容量
import re
from dataCollect.analysis.SpecRefer import brand_refer, trans
import pandas as pd

def ramInfo(store, category, description):
        
    def coolpc(category,description):
        #  品牌(brand)
        brand = "NG"
        for i in brand_refer["ramLst"]:
            if i == "":
                break
            elif str.upper(i) in str.upper(description):
                brand = i
                break
        for j in brand_refer["ramLstE"]:
            if brand != "NG" or j == "":
                break
            elif str.upper(j) in str.upper(description):
                brand = trans(j)
                break
        
        # DIMM(dimm)
        if "DDR" in str.upper(category) and "筆記型" not in str.upper(category) and "伺服器" not in str.upper(category):
            dimm = re.findall(r"DDR\d",str.upper(category))[0]
        else:
            dimm = "NG"
    
        # 通道數(channel)
        if "筆記型" in category or "伺服器" in category:
            channel = "NG"
        else:
            if "雙通道" in category:
                channel = "雙通道"
            elif "四通道" in category:
                channel = "四通道"
            else:
                channel = "單條"
    
    
        # 容量 (capacity)
        if "筆記型" in category or "伺服器" in category:
            capacity = "NG"
        else:
            if "雙通道" in category or "四通道" in category:
                temp1 = re.findall(r"\d{1,3}GB\*\d",str.upper(description)) # 正常狀況
                temp2 = re.findall(r"\d{1,3}G\*\d",str.upper(description)) # 有些會只有 G ，也就是會是 G*2 而不是 GB*2
                if len(temp1) > 0:
                    capacity = eval(temp1[0].split("GB*")[0])
                    # qty = eval(temp1[0].split("GB*")[1])
                elif len(temp2) > 0:
                    capacity = eval(temp2[0].split("G*")[0])
                    # qty = eval(temp2[0].split("G*")[1])
                else:
                    capacity = "NG"
            else:
                temp = re.findall(r"\d{1,3}GB",str.upper(description))
                if len(temp) > 0:
                    capacity = eval(temp[0].split("GB")[0])
                    # qty = eval(temp1[0].split("GB*")[1])
                else:
                    capacity = "NG"
        capUnit = "GB"


        return brand, dimm, channel, capacity, capUnit
        
    def newton(category,description):
        #  品牌(brand)
        brand = "NG"
        for i in brand_refer["ramLst"]:
            if i == "":
                break
            elif str.upper(i) in str.upper(description):
                brand = i
                break
        for j in brand_refer["ramLstE"]:
            if brand != "NG" or j == "":
                break
            elif str.upper(j) in str.upper(description):
                brand = trans(j)
                break
        
        # DIMM(dimm)
        if "DDR" in str.upper(category) and "SODIMM" not in str.upper(category) and "伺服器" not in str.upper(category):
            dimm = re.findall(r"DDR\d",str.upper(category))[0]
        else:
            dimm = "NG"
    
        # 通道(channel)
        if "SODIMM" in category or "伺服器" in category:
            channel = "NG"
        else:
            if "雙通道" in description:
                channel = "雙通道"
            elif "四通道" in description:
                channel = "四通道"
            else:
                channel = "單條"
    
    
        # 容量 (capacity)
        if "SODIMM" in category or "伺服器" in category:
            capacity = "NG"
        else:
            if "雙通道" in description or "四通道" in description:
                temp1 = re.findall(r"\d{1,3}GB\*\d",str.upper(description)) # 正常狀況
                temp2 = re.findall(r"\d{1,3}G\*\d",str.upper(description)) # 有些會只有 G ，也就是會是 G*2 而不是 GB*2
                if len(temp1) > 0:
                    capacity = eval(temp1[0].split("GB*")[0])
                    # qty = eval(temp1[0].split("GB*")[1])
                elif len(temp2) > 0:
                    capacity = eval(temp2[0].split("G*")[0])
                    # qty = eval(temp2[0].split("G*")[1])
                else:
                    capacity = "NG"
            else:
                temp = re.findall(r"\d{1,3}GB",str.upper(description))
                if len(temp) > 0:
                   temp = re.findall(r"\d{1,3}GB",str.upper(description)) # 正常狀況
                   capacity = eval(temp[0].split("GB")[0])
                    # qty = eval(temp1[0].split("GB*")[1])
                else:
                    capacity = "NG"
        capUnit = "GB"
    
    
        return brand, dimm, channel, capacity, capUnit

    
    if store == "coolpc":
        brand, dimm, channel, capacity, capUnit = coolpc(category,description)
    elif store == "newton":
        brand, dimm, channel, capacity, capUnit = newton(category,description)

    return brand, dimm, channel, capacity, capUnit


if __name__ == "__main__":
    
    #################### 測試資料 ####################
    data = pd.read_csv("nt-.csv",delimiter=",",encoding="ANSI")
    data1 = data[data["類別"] == "記憶體 RAM"]["子類別"]
    data2 = data[data["類別"] == "記憶體 RAM"]["品名"]
    ##################################################

    k = 0
    for i,j in zip(data1,data2):
        brand, dimm, channel, capacity, capUnit = ramInfo("newton", i,j)
        if brand == "NG" or dimm == "NG" or channel == "NG" or capacity == "NG" or capUnit == "NG":
            continue
        print(brand,end=" \ ")
        print(dimm,end=" \ ")
        print(channel,end=" \ ")
        print(str(capacity)+capUnit,end=" \ ")
        # print(size,end=" \ ")
        k += 1
        print(k)