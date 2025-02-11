from django.test import TestCase
from dataCollect.models import partList

def dbtest():
    # 此處是將資料庫的資料統整出每個分類的每個選單中，有哪些選項。
    # 將統整的資料作成一個名為 specifications 的 JSON 格式資料，將用於回傳給前端
    # 目前問題是當 CPU 選擇了 Intel 後，其他選項仍會連同 AMD 的一同顯示，沒有即時篩選功能。將使用字典中的字典來配合渲染網頁的篩選功能解決這個問題。

    itemNames = {
    "處理器 CPU":["品牌","世代","腳位","型號","有無內顯"],
    "主機板 MB":["品牌","晶片組","DIMM","腳位","尺寸"],
    "記憶體 RAM":["品牌","架構","通道數","容量",""],
    "顯示卡 Video":["品牌","陣營","晶片","長度","GDDR"],
    "固態硬碟 SSD":["品牌","介面","容量","",""],
    "硬碟 HDD":["品牌","尺寸","應用","容量","轉速"],
    "機殼 CASE":["品牌","尺寸","側板","靜音",""],
    "電源供應器 POWER":["品牌","瓦數","效率等級","靜音",""],
    "CPU空冷散熱器":["品牌","高度","導管","散熱方式",""]
    }

    specifications = {}

    for i in itemNames:
        data = partList.objects.filter(category = i)
        brands = set()
        spec1s = set()    
        spec2s = set()
        spec3s = set()
        spec4s = set()

        for j in data:
            brands.add(j.brand)
        for j in data:
            spec1s.add(j.spec1)
        for j in data:
            spec2s.add(j.spec2)
        for j in data:
            spec3s.add(j.spec3)
        for j in data:
            spec4s.add(j.spec4)

        brands = list(brands)
        spec1s = list(spec1s)
        spec2s = list(spec2s)
        spec3s = list(spec3s)
        spec4s = list(spec4s)

        specs[i] = {itemNames[i][0]:brands,itemNames[i][1]:spec1s,itemNames[i][2]:spec2s,itemNames[i][3]:spec3s,itemNames[i][4]:spec4s}

        return specifications