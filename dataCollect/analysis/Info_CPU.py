# Info_CPU-v1.0
# 由於目前同樣的 code 對 coolpc 和 newton 都能判斷，所以目前只使用一組程式碼。
import re
import pandas as pd
from dataCollect.analysis.SpecRefer import brand_refer, trans

# CPU：品牌(brand)、世代別(gen)、型號(model:i3,i5,i7,i9)、有無內顯(gpu_in)、有無風扇(fan)

def cpuInfo(store, category, description):

    def cpu(category,description):
        #  品牌
        if "intel" in str.lower(category):
            brand = "Intel"
        elif "amd" in str.lower(category):
            brand = "AMD"
        else:
            brand = "NG"
            
        # 代別
        gen = "NG"
        if brand == "Intel":
            temp = re.findall(r"\d{2}代",str.upper(category))
            if len(temp) > 0:
                gen = temp[0]
        elif brand == "AMD":
            temp1 = re.findall(r"R\d{1,2}[^0-9]\d{4,5}",str.upper(description))
            if len(temp1) > 0:
                temp2 = re.findall(r"\d{4,5}",temp1[0])[0]
                gen = temp2[0]+"000 系列"
            
        # 型號
        model = gpu_in = fan = "NG"
        if brand == "Intel":
            temp = re.findall(r"I\d{1}.\d+[a-zA-Z]{,3}",str.upper(description))
            if len(temp) > 0:
                model = str.lower(re.findall(r"I\d{1,3}",temp[0])[0])
                tail_letter = re.findall(r"[a-zA-Z]{,3}$",temp[0])[0]
                if "F" in tail_letter:
                    gpu_in = "N"
                else:
                    gpu_in = "Y"
                if "K" in tail_letter:
                    fan = "N"
                else:
                    fan = "Y"
        elif brand == "AMD":
            temp = re.findall(r"R\d{1}[^0-9]\d{4,5}[a-zA-Z]{,3}",str.upper(description)) # 因型號數字是5位數時，避免第5尾數被當作尾號的第一位，因此先取出尾號前的部分
            if len(temp) > 0:
                model = re.findall(r"R\d{1,2}",temp[0])[0]
                tail_letter = re.findall(r"[a-zA-Z]{,3}$",temp[0])[0]
                if "F" in tail_letter:
                    gpu_in = "N"
                else:
                    gpu_in = "Y"
                fan = "Y"
        
        # 腳位
        socket = "NG"
        if brand == "Intel":
            temp = re.findall(r"\d{4,5} ?腳位",category)
            if len(temp) > 0:
                socket = re.findall(r"^\d{4,5}",temp[0])[0]+"腳位"
        elif brand == "AMD":
            temp = re.findall(r"AM\d",category)
            if len(temp) > 0:
                socket = temp[0]
        
        return brand, gen, socket, model, gpu_in, fan

    if store == "coolpc":
        brand, gen, socket, model, gpu_in, fan = cpu(category,description)
    elif store == "newton":
        brand, gen, socket, model, gpu_in, fan = cpu(category,description)

    return brand, gen, socket, model, gpu_in, fan


if __name__ == "__main__":

    #################### 測試資料 ####################
    data = pd.read_csv("cp-.csv",delimiter=",",encoding="ANSI")
    data1 = data[data["類別"] == "處理器 CPU"]["子類別"]
    data2 = data[data["類別"] == "處理器 CPU"]["品名"]
    ##################################################

    k = 0
    for i,j in zip(data1,data2):
        brand, gen, socket, model, gpu_in, fan = cpuInfo("coolpc",i,j)
        if brand == "NG" or gen == "NG" or socket == "NG" or model == "NG" or gpu_in == "NG" or fan == "NG":
            continue
        print(brand,end=" \ ")
        print(gen,end=" \ ")
        print(socket,end=" \ ")
        print(model,end=" \ ")
        print(gpu_in,end=" \ ")
        print(fan,end=" \ ")
        k += 1
        print(k)