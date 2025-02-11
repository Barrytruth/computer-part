# 前端選擇查詢的條件回傳後：
# 將 spec1、spec2、spec3、spec4，衍生出一組虛擬欄位：篩選需要比較大小的欄位時，會先將字串型態數字轉成數值型態數字，儲存在虛擬欄位

from dataCollect.models import partList
from frontData.menus import  itemNames
from django.db.models import Case, When, F, FloatField, CharField
from django.db.models.functions import Cast
import re

# condition2Cast  判斷並處理將前端回傳的篩選條件
#  - 傳入的 db_field：參照的欄位名稱，目前會帶入的只有 spec1、spec2、spec3、spec4，以下統稱 spec*，用於決定篩選比對的對象欄位的名稱；
#  - 傳入的 condition：前端傳回的此欄的篩選條件
#  (1) 篩選條件中有">"、"<"或"="的，抽取其中數字並作單位換算。
#  (2) 篩選條件中有">"、"<"或"="的，篩選對象是虛擬欄位，以及篩選方式；   (虛擬欄位就是在queryset 中使用 .annotate() 方法產生的虛擬欄位。)
#      例如若參照的資料庫欄位是 spec1，虛擬欄位就是 spec1trans。
#  (3) 單位換算：由於目前只有 GB 和 TB 會混在一起，因此統一換算成 GB，其餘使用 cm、W 等單位的數值，因為資料庫資料和篩選條件都是相同單位，因此不作換算，可以直接比對數字。
#  (4) 篩選條件中  沒有  ">"、"<"或"="的，篩選對象是參照的資料庫欄位。
#  (5) 篩選條件中有">"、"<"或"="的，回傳的 value 就是篩選條件轉換好的浮點數數值，也就是浮點數數值的篩選條件。
#  (6) 篩選條件中  沒有  ">"、"<"或"="的，回傳的 value 就是未經轉換的篩選條件，也就是字串型態的純文字的篩選條件。
#  (7) 篩選方式：">"是在虛擬欄位名稱後面加上查詢表達式 __gt；"<"是加上 __lt；"="不加上查詢表達式，也就是虛擬欄位名稱，在這裡就是 db_field+"trans。
#  (8) 最後是以鍵值對 return 篩選對象、篩選條件和篩選方式，就是： 篩選對象欄位_篩選方式:篩選條件值()
#      基礎邏輯是：需要比較大小的篩選條件將對虛擬欄位作"大小比較"的篩選，其餘欄位對原資料庫欄位作"字串比對"的篩選。
def condition2Cast(db_field,condition): # 判斷並處理前端回傳的篩選條件

    print("dataFilter/condition2Cast：處理前端回傳的篩選條件")

    if ">" in condition or "<" in condition or "="in condition:
        num = eval(re.findall(r"\d+\.?\d*",condition)[0]) # 抽取出 >65GB 字樣的數值部分
        unT = re.findall(r"[a-zA-Z]{1,3}$",condition)[0] # 抽取出 >65GB 字樣的單位部分
        if unT == "TB":
            value = num*1024
        if ">" in condition:
            filterName = db_field+"trans__gt"
            value = num
        elif "<" in condition:
            filterName = db_field+"trans__lt"
            value = num
        elif "=" in condition:
            filterName = db_field+"trans"
            value = num
    else:
        filterName = db_field
        value = condition
    return filterName, value

    ################################################## 獲取並處理：前端 POST 資料 ##################################################
    # 這些是前端選單回傳的"選擇結果"，和資料庫資料還沒關係
    # itemNames[category][] 只是借用 menus 的字典抽取出每個分類在規格欄有哪幾個規格項名稱，因為前端是以規格項名稱傳遞資料，所以這裡必須知道規格項名稱才能接收
    # 這裡欄位變數名稱前面的 "C" 代表 Condition，也就是代表"查詢條件"

def partFilter(request):
    
    print("dataFilter/condition2Cast：取得前端回傳之篩選條件")

    # 前端選單回傳的"選擇結果"
    categoryC = request.POST.get('category', "")              # 前端選擇的"分類"
    brandC = request.POST.get('brand', "")                    # 前端選擇的"分類"
    spec1C = request.POST.get(itemNames[categoryC][1], "")    # 先以前端選擇麼"分類名稱"透過 itemName 字典查到查詢該分類所有欄位的名稱，並取得第2個欄位名稱，再以此取得前端同名欄位的選擇結果。
    spec2C = request.POST.get(itemNames[categoryC][2], "")    # 同上，取得第3個欄位名稱，再以此欄位名稱取得前端回傳的同名欄位名稱的選擇結果。
    spec3C = request.POST.get(itemNames[categoryC][3], "")    # 同上...取得第4個欄位名稱...
    spec4C = request.POST.get(itemNames[categoryC][4], "")    # 同上...取得第5個欄位名稱...

    # 印出接收到的資料 for debug
    print("分類:", categoryC)
    print(itemNames[categoryC][0]+"：", brandC)
    print(itemNames[categoryC][1]+"：", spec1C)
    print(itemNames[categoryC][2]+"：", spec2C)
    print(itemNames[categoryC][3]+"：", spec3C)
    print(itemNames[categoryC][4]+"：", spec4C)

    # 由於資料庫中所有資料都是字串型態，即使是數字都是字串型態的數字，無法作">"、"<"或"="的比較並篩選，因此將包含有">"、"<"或"="的篩選條件擷取數字，轉換成浮點數型態並作單位轉換後，
    # 建立虛擬欄位，並將轉換好的數值存入虛擬欄位。
    #  - 參照 spec1 欄位的，虛擬欄位就是 spec1trans，spec1trans 是在 queryset 中使用 .annotate() 方法產生的虛擬欄位。
    #  - 單位換算：由於目前只有 GB 和 TB 會混在一起，因此統一換算成 GB，其餘使用 cm、W 等單位的數值，因為資料庫資料和篩選條件都是相同單位，因此不作換算，可以直接比對數字。
    #  - Django 的 Case 和 When 條件判斷是以「第一個匹配的條件」為基準。當某個 When 條件的判斷為真（例如 When(unit1="Tb", ...)），那麼對應的 then 子句會被執行，並且後續的 When 條件就會被跳過。
    #    When 條件都不符合時，才會執行 default。這裡沒有 default 是因為只處理需要比較大小的欄位的數字資料，處理完成的數值放入虛擬欄位。其他欄位資料不在這裡處理。
    #    也就是虛擬欄位只有需要比較大小的欄位的資料，且是數值型態、經過單位轉換的數值資料。

    queryset = partList.objects.annotate(
        spec1trans = Case(
            When(unit1="TB", then=Cast(("spec1"),FloatField())*1024),  # TB → GB
            When(spec1__regex=r"^\d+\.?\d+$", then=Cast(("spec1"),FloatField()))), # 其他數值保持不變
        spec2trans = Case(
            When(unit2="TB", then=Cast(("spec2"),FloatField())*1024),  # TB → GB
            When(spec2__regex=r"^\d+\.?\d+$", then=Cast(("spec2"),FloatField()))),
        spec3trans = Case(
            When(unit3="TB", then=Cast(("spec3"),FloatField())*1024),  # TB → GB
            When(spec3__regex=r"^\d+\.?\d+$", then=Cast(("spec3"),FloatField()))),
        spec4trans = Case(
            When(unit4="TB", then=Cast(("spec4"),FloatField())*1024),  # TB → GB
            When(spec4__regex=r"^\d+\.?\d+$", then=Cast(("spec4"),FloatField())))
        )

    # 將篩選條件做成字典型態資料，帶入 .filter() 後，.filter() 會將其轉換成篩選語法並進行篩選
    filters = {}

    if categoryC:
        filters['category'] = categoryC
    if brandC:
        filters['brand'] = brandC
    if spec1C:
        key, value = condition2Cast("spec1",spec1C)
        filters[key] = value
    if spec2C:
        key, value = condition2Cast("spec2",spec2C)
        filters[key] = value
    if spec3C:
        key, value = condition2Cast("spec3",spec3C)
        filters[key] = value
    if spec4C:
        key, value = condition2Cast("spec4",spec4C)
        filters[key] = value

    filteredData = queryset.filter(**filters)

    print("dataFilter/condition2Cast：篩選完成")

    result = [] # 串列中，每一筆資料是一個字典，每個字典是資料庫的一筆資料的部分欄位

    for obj in filteredData:
        result.append({
        "id":obj.id,
        "store" : obj.store,
        "category" : obj.category,
        "description" : obj.description,
        "orgPrice" : obj.orgPrice,
        "saleEnd" : obj.saleEnd,
        "price" : obj.price})

    print("dataFilter/condition2Cast：回傳篩選完成之資料")

    return result