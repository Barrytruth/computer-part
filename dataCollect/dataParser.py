from dataCollect.analysis.Info_CASE import caseInfo
from dataCollect.analysis.Info_CPU import cpuInfo
from dataCollect.analysis.Info_HDD import hddInfo
from dataCollect.analysis.Info_HeatSink import heatsinkInfo
from dataCollect.analysis.Info_MB import mbInfo
from dataCollect.analysis.Info_PSU import psuInfo
from dataCollect.analysis.Info_RAM import ramInfo
from dataCollect.analysis.Info_SSD import ssdInfo
from dataCollect.analysis.Info_VIDEO import videoInfo
from dataCollect.models import partList
import pandas as pd

print("----- Importing dataParser")

idLst = []
brandLst = []
spec1Lst = []
unit1Lst = []
spec2Lst = []
unit2Lst = []
spec3Lst = []
unit3Lst = []
spec4Lst = []
unit4Lst = []

def analysis():
    # 剖析 CPU 資料
    data = partList.objects.filter(category="處理器 CPU")
    for i in data:

        if i.store == "原價屋":
            brand, gen, socket, model, gpu_in, fan = cpuInfo("coolpc",i.sub_cate,i.description)
        elif i.store == "紐頓":
            brand, gen, socket, model, gpu_in, fan = cpuInfo("newton",i.sub_cate,i.description)

        # 將擷取的關鍵字加入相對應的字串
        idLst.append(i.id)
        brandLst.append(brand)
        spec1Lst.append(gen)
        unit1Lst.append("－")
        spec2Lst.append(socket)
        unit2Lst.append("－")
        spec3Lst.append(model)
        unit3Lst.append("－")
        spec4Lst.append(gpu_in)
        unit4Lst.append("－")
    print("完成CPU資料解析")

    # 剖析 主機板 資料
    data = partList.objects.filter(category="主機板 MB")
    for i in data:

        if i.store == "原價屋":
            brand, chipset, dimm, socket, size = mbInfo("coolpc",i.sub_cate,i.description)
        elif i.store == "紐頓":
            brand, chipset, dimm, socket, size = mbInfo("newton",i.sub_cate,i.description)

        # 將擷取的關鍵字加入相對應的字串
        idLst.append(i.id)
        brandLst.append(brand)
        spec1Lst.append(chipset)
        unit1Lst.append("－")
        spec2Lst.append(dimm)
        unit2Lst.append("－")
        spec3Lst.append(socket)
        unit3Lst.append("－")
        spec4Lst.append(size)
        unit4Lst.append("－")
    print("完成主機板資料解析")

    # 剖析 RAM 資料
    data = partList.objects.filter(category="記憶體 RAM")
    for i in data:

        if i.store == "原價屋":
            brand, dimm, channel, capacity, capUnit = ramInfo("coolpc",i.sub_cate,i.description)
        elif i.store == "紐頓":
            brand, dimm, channel, capacity, capUnit = ramInfo("newton",i.sub_cate,i.description)

        # 將擷取的關鍵字加入相對應的字串
        idLst.append(i.id)
        brandLst.append(brand)
        spec1Lst.append(dimm)
        unit1Lst.append("－")
        spec2Lst.append(channel)
        unit2Lst.append("－")
        spec3Lst.append(capacity)
        unit3Lst.append(capUnit)
        spec4Lst.append("－")
        unit4Lst.append("－")
    print("完成RAM資料解析")

    # 剖析 顯示卡 資料
    data = partList.objects.filter(category="顯示卡 Video")
    for i in data:

        if i.store == "原價屋":
            brand, camp, vchip, length, lenUnit, gddr, gddrUnit = videoInfo("coolpc",i.sub_cate,i.description)
        elif i.store == "紐頓":
            brand, camp, vchip, length, lenUnit, gddr, gddrUnit = videoInfo("newton",i.sub_cate,i.description)

        # 將擷取的關鍵字加入相對應的字串
        idLst.append(i.id)
        brandLst.append(brand)
        spec1Lst.append(camp)
        unit1Lst.append("－")
        spec2Lst.append(vchip)
        unit2Lst.append("－")
        spec3Lst.append(length)
        unit3Lst.append(lenUnit)
        spec4Lst.append(gddr)
        unit4Lst.append(gddrUnit)
    print("完成顯示卡資料解析")

    # 剖析 SSD 資料
    data = partList.objects.filter(category="固態硬碟 SSD")
    for i in data:

        if i.store == "原價屋":
            brand, interface, capacity, capUnit = ssdInfo("coolpc",i.sub_cate,i.description)
        elif i.store == "紐頓":
            brand, interface, capacity, capUnit = ssdInfo("newton",i.sub_cate,i.description)

        # 將擷取的關鍵字加入相對應的字串
        idLst.append(i.id)
        brandLst.append(brand)
        spec1Lst.append(interface)
        unit1Lst.append("－")
        spec2Lst.append(capacity)
        unit2Lst.append(capUnit)
        spec3Lst.append("－")
        unit3Lst.append("－")
        spec4Lst.append("－")
        unit4Lst.append("－")
    print("完成SSD資料解析")

    # 剖析 HDD 資料
    data = partList.objects.filter(category="硬碟 HDD")
    for i in data:

        if i.store == "原價屋":
            brand, size, use, capacity, capUnit, rpm = hddInfo("coolpc",i.sub_cate,i.description)
        elif i.store == "紐頓":
            brand, size, use, capacity, capUnit, rpm = hddInfo("newton",i.sub_cate,i.description)

        # 將擷取的關鍵字加入相對應的字串
        idLst.append(i.id)
        brandLst.append(brand)
        spec1Lst.append(size)
        unit1Lst.append("－")
        spec2Lst.append(use)
        unit2Lst.append("－")
        spec3Lst.append(capacity)
        unit3Lst.append(capUnit)
        spec4Lst.append(rpm)
        unit4Lst.append("－")
    print("完成硬碟資料解析")

    # 剖析 機殼 資料
    data = partList.objects.filter(category="機殼 CASE")
    for i in data:

        if i.store == "原價屋":
            brand, size, gside, silence = caseInfo("coolpc",i.sub_cate,i.description)
        elif i.store == "紐頓":
            brand, size, gside, silence = caseInfo("newton",i.sub_cate,i.description)

        # 將擷取的關鍵字加入相對應的字串
        idLst.append(i.id)
        brandLst.append(brand)
        spec1Lst.append(size)
        unit1Lst.append("－")
        spec2Lst.append(gside)
        unit2Lst.append("－")
        spec3Lst.append(silence)
        unit3Lst.append("－")
        spec4Lst.append("－")
        unit4Lst.append("－")
    print("完成機殼資料解析")

    # 剖析 PSU 資料
    data = partList.objects.filter(category="電源供應器 POWER")
    for i in data:

        if i.store == "原價屋":
            brand, walt, waltUnit, grade, modular, silence = psuInfo("coolpc",i.sub_cate,i.description)
        elif i.store == "紐頓":
            brand, walt, waltUnit, grade, modular, silence = psuInfo("newton",i.sub_cate,i.description)

        # 將擷取的關鍵字加入相對應的字串
        idLst.append(i.id)
        brandLst.append(brand)
        spec1Lst.append(walt)
        unit1Lst.append(waltUnit)
        spec2Lst.append(grade)
        unit2Lst.append("－")
        spec3Lst.append(modular)
        unit3Lst.append("－")
        spec4Lst.append(silence)
        unit4Lst.append("－")
    print("完成電源供應器資料解析")

    # 剖析 CPU空冷散熱器 資料
    data = partList.objects.filter(category="CPU空冷散熱器")
    for i in data:

        if i.store == "原價屋":
            brand, height, hUnit, pipe, direct = heatsinkInfo("coolpc",i.sub_cate,i.description)
        elif i.store == "紐頓":
            brand, height, hUnit, pipe, direct = heatsinkInfo("newton",i.sub_cate,i.description)

        # 將擷取的關鍵字加入相對應的字串
        idLst.append(i.id)
        brandLst.append(brand)
        spec1Lst.append(height)
        unit1Lst.append(hUnit)
        spec2Lst.append(pipe)
        unit2Lst.append("－")
        spec3Lst.append(direct)
        unit3Lst.append("－")
        spec4Lst.append("－")
        unit4Lst.append("－")
    print("完成CPU空冷散熱器資料解析")

    parsedData = pd.DataFrame({"id":idLst,"brand":brandLst,"spec1":spec1Lst,"unit1":unit1Lst,
                               "spec2":spec2Lst,"unit2":unit2Lst,"spec3":spec3Lst,"unit3":unit3Lst,"spec4":spec4Lst,"unit4":unit4Lst})
    
    return parsedData