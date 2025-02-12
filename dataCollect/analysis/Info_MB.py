# Info_MB-v1.1
# 由於目前只打算以四個 spec 欄位顯示所有規格相關資訊，但是使用者會需要看到 cpubrand，只看晶片組不夠直觀，如此一來主機板會有5個欄位的需求，
# 因此將 cpubrand 加入 chipset 合併為一個欄位，也就是在原本的 chipset 欄位合併
import re
from dataCollect.analysis.SpecRefer import brand_refer, trans
import pandas as pd

# MB：品牌(brand)、CPU陣營、晶片組、尺寸

def mbInfo(store, category, description):

    def mb(category,description):
        #  品牌(brand)
        brand = "NG"
        for i in brand_refer["mbLst"]:
            if i == "":
                break
            elif str.upper(i) in str.upper(description):
                brand = i
                break
        for j in brand_refer["mbLstE"]:
            if brand != "NG" or j == "":
                break
            elif str.upper(j) in str.upper(description):
                brand = trans(j)
                break
        # 先取得CPU廠牌
        if "INTEL" in str.upper(category):
            cpubrand = "INTEL"
        elif "AMD" in str.upper(category):
            cpubrand = "AMD"
        else:
            cpubrand = "NG"
        
        # 晶片組(chipset)
        chipset = "NG"
        if cpubrand == "INTEL":
            temp1 = re.findall(r"INTEL [A-Z]\d{2,3}",str.upper(category))
            if len(temp1) > 0:
                chipset = "Intel：" + re.findall(r"[A-Z]\d{2,3}",temp1[0])[0]
        elif cpubrand == "AMD":
            temp2 = re.findall(r"AMD [A-Z]\d{2,3}",str.upper(category))
            if len(temp2) > 0:
                chipset = "AMD：" + re.findall(r"[A-Z]\d{2,3}",temp2[0])[0]
            
        # DIMM(dimm)
        if "DDR" in str.upper(category):
            dimm = re.findall(r"DDR\d",str.upper(category))[0]
        else:
            dimm = "NG"
    
        # 腳位(socket)
        if cpubrand == "INTEL":
            temp1 = re.findall(r"\d{4}.?腳位",str.upper(category))
            if len(temp1) > 0:
                socket = re.findall(r"\d{4}",temp1[0])[0]+"腳位"
            else:
                socket = "NG"
        elif cpubrand == "AMD":
            temp2 = re.findall(r"AM\d",category)
            if len(temp2) > 0:
                socket = temp2[0]
            else:
                socket = "NG"
        else:
            socket = "NG"
    
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
            if "MINI-ATX" in str.upper(description):
                size = "MINI-ITX"
            else:
                size = "ITX"
    
        return brand, chipset, dimm, socket, size

        
    if store == "coolpc":
        brand, chipset, dimm, socket, size = mb(category,description)
    elif store == "newton":
        brand, chipset, dimm, socket, size = mb(category,description)

    return brand, chipset, dimm, socket, size


if __name__ == "__main__":
    
    #################### 測試資料 ####################
    data = pd.read_csv("cp-.csv",delimiter=",",encoding="ANSI")
    data1 = data[data["類別"] == "主機板 MB"]["子類別"]
    data2 = data[data["類別"] == "主機板 MB"]["品名"]
    ##################################################
    
    k = 0
    for i,j in zip(data1,data2):
        brand, chipset, dimm, socket, size = mbInfo("coolpc",i,j)
        if brand == "NG" or chipset == "NG" or dimm == "NG" or socket == "NG" or size == "NG":
            continue
        print(brand,end=" \\ ")
        print(chipset,end=" \\ ")
        print(dimm,end=" \\ ")
        print(socket,end=" \\ ")
        print(size,end=" \\ ")
        k += 1
        print(k)