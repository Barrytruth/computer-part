from django.shortcuts import render
from frontData.menus import menuItem
from frontData.menus import unitOptions
from frontData.dataFilter import partFilter
import json
from django.http import JsonResponse

# 🔹 Home 頁面
def home(request):
    specifications = menuItem()
    return render(request, "home.html", {"specifications": specifications, "unit_options": unitOptions})

# 🔹 處理篩選條件
def dataRequest(request):
    results = partFilter(request)
    specifications = menuItem()
    return render(request, "home.html", {"specifications": specifications, "unit_options": unitOptions, "results": results})

# 🔹 取得已選擇的項目
def get_selected_items(request):
    selected_items = request.session.get("selectedItems", [])
    return JsonResponse({"selected_items": selected_items})

# 🔹 提交選擇的項目，**追加**到 session，而不是覆蓋
def submitSelection(request): # POST
    # 取得前端回傳勾選資料
    data = json.loads(request.body)  # 解析 JSON 資料
    
    # 抽取資料
    new_selected_items = data.get("selected_items", []) # [篩選結果]表單資料
    ordered_list = data.get("orderedList", []) # [零組件選擇清單]表單資料

    # 追加新選擇的項目，同時避免重複
    for item in new_selected_items:
        if item not in ordered_list:
            ordered_list.append(item)

    # 更新 session
    request.session["selectedItems"] = ordered_list
    request.session.set_expiry(3600)  # 設定 1 小時後過期
    return JsonResponse({"status": "success", "message": "選擇已儲存"})

# 🔹 清除所有選擇的項目
def clear_selection(request): # POST
    request.session["selectedItems"] = []  # 清空 session
    print("所有選擇已清除")
    return JsonResponse({"status": "success", "message": "所有選擇已清除"})