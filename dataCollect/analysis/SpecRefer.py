# SpecRefer 1.0
import pandas as pd
import re

#################### brand 清單 #####################
# 若有增加類別，須將類別新增至 for迴圈 以及 DataFrame
mbLst = ["華碩", "技嘉", "微星", "華擎","恩傑"]
mbLstE = ["ASUS", "GIGABYTE", "MSI", "ASROCK", "NZXT"]
videoLst = ["華碩", "技嘉", "微星", "華擎", "INNO3D", "ZOTAC", "撼訊"]
videoLstE = ["ASUS", "GIGABYTE", "MSI", "ASROCK", "INNO3D", "ZOTAC", "TUL"]
ramLst= ["UMAX", "威剛", "金士頓", "美光", "宏碁", "芝奇", "十銓", "科賦", "巨蟒", "海盜船"]
ramLstE= ["UMAX", "ADATA", "KINGSTON", "MICRON", "ACER", "G.SKILL", "TEAMGROUP", "KLEVV", "ANACOMDA", "CORSAIR"]
hdLst = ["東芝", "希捷", "WD "]
hdLstE = ["Toshiba", "SEAGATE", "WD "]
ssdLst = ["UMAX", "威剛", "WD ", "金士頓", "十銓", "宏碁", "美光", "三星", "海力士", "希捷", "SOLIDIGM", "巨蟒", "微星", "科賦","鎧俠"]
ssdLstE = ["UMAX", "ADATA", "WD ", "KINGSTON", "TEAMGROUP", "ACER", "MICRON", "SAMSUNG", "SK ", "SEAGATE", "SOLIDIGM", "ANACOMDA", "MSI",
           "KLEVV","KIOXIA"]
caseLst = ["聯力","酷碼","全漢","銀欣","abee","Fractal Design","喬思伯","華碩","視博通","君主","微星","技嘉","大飛","美洲獅","先馬","旋剛",
           "安鈦克","火鳥","美商艾湃","HYTE","追風者","恩傑","幾何未來","威剛","曜越","SSUPD","九州風神","安耐美(保銳)","松聖","迎廣","海盜船",
           "亞碩","首席玩家","賽德斯","i-coolTW","IMAX","XPG","微星"]
caseLstE = ["LIAN LI", "CoolerMaster", "FSP", "SilverStone", "abee", "Fractal Design", "JONSBO", "ASUS", "Superchannel", "Montech", "MSI",
            "GIGABYTE", "darkFlash", "COUGAR", "SAMA", "Sharkoon", "Antec", "BitFenix", "Apexgaming", "HYTE", "Phanteks", "NZXT", "Geometric Future",
            "ADATA","Thermaltake","SSUPD","DEEPCOOL","ENERMAX","Mavoly","InWin","Corsair","亞碩","1st Player","SADES","i-coolTW",
            "IMAX","XPG","MSI"]
psuLst = ["華碩","海韻","全漢","酷碼","技嘉","曜越","台達","銀欣","安耐美(保銳)","振華","美商艾湃","火鳥","美洲獅","君主","恩傑","九州風神",
          "微星","海盜船","安鈦克","聯力","XPG","松聖","Fractal Design","七盟"]
psuLstE = ["ASUS","SeaSonic","FSP","CoolerMaster","GIGABYTE","Thermaltake","Delta","SilverStone","ENERMAX","Super Flower","Apexgaming",
           "BitFenix", "COUGAR","Montech","NZXT","DEEPCOOL","MSI","Corsair","Antec","LIAN LI","XPG","Mavoly","Fractal Design","Seventeam"]
heatsinkLst = ["利民","美洲獅","ID-COOLING","君主","九州風神","銀欣","酷碼","鎌刀","喬思伯","貓頭鷹","快睿","全漢","富鈞","黑豹","大飛"]
heatsinkLstE = ["Thermalright","COUGAR","ID-COOLING","Montech","DEEPCOOL","SilverStone","CoolerMaster","Scythe","JONSBO","Noctua",
                "CRYORIG","FSP","XIGMATEK","be quiet!","darkFlash"]


longestLst = 0
cate_list = [mbLst,videoLst,ramLst,hdLst,ssdLst,caseLst,psuLst,heatsinkLst]
for i in cate_list:
    if longestLst < len(i):
        longestLst = len(i)

brand_refer = pd.DataFrame({
    "mbLst":mbLst + [""]*(longestLst-len(mbLst)),
    "mbLstE":mbLstE + [""]*(longestLst-len(mbLstE)),
    "videoLst":videoLst + [""]*(longestLst-len(videoLst)),
    "videoLstE":videoLstE + [""]*(longestLst-len(videoLstE)),
    "ramLst":ramLst + [""]*(longestLst-len(ramLst)),
    "ramLstE":ramLstE + [""]*(longestLst-len(ramLstE)),
    "hdLst":hdLst + [""]*(longestLst-len(hdLst)),
    "hdLstE":hdLstE + [""]*(longestLst-len(hdLstE)),
    "ssdLst":ssdLst + [""]*(longestLst-len(ssdLst)),
    "ssdLstE":ssdLstE + [""]*(longestLst-len(ssdLstE)),
    "caseLst":caseLst + [""]*(longestLst-len(caseLst)),
    "caseLstE":caseLstE + [""]*(longestLst-len(caseLstE)),
    "psuLst":psuLst + [""]*(longestLst-len(psuLst)),
    "psuLstE":psuLstE + [""]*(longestLst-len(psuLstE)),
    "heatsinkLst":heatsinkLst + [""]*(longestLst-len(heatsinkLst)),
    "heatsinkLstE":heatsinkLstE + [""]*(longestLst-len(heatsinkLstE))
    })
#####################################################

###################### 中英對照 ######################
cht = mbLst+videoLst+ramLst+hdLst+ssdLst+caseLst+psuLst+heatsinkLst
eng = mbLstE+videoLstE+ramLstE+hdLstE+ssdLstE+caseLstE+psuLstE+heatsinkLstE

eng_C = dict(zip(eng,cht))
cht_E = dict(zip(cht,eng))

def trans(word):
    check_E = re.findall(r"[0-9a-zA-Z]+",str.upper(word))
    check_C = re.findall(r"[\u4e00-\u9fa5]+",str.upper(word))
    if len(check_E) > 0:
        ans = eng_C[word]
    elif len(check_C) > 0:
        ans = cht_E[word]
    return ans

###################### 錯字更正 ######################
rpswrds = {"酷媽":"酷碼","LAN":"LAIN","安耐美":"安耐美(保銳)","保銳":"安耐美(保銳)"}
def correct(string):
    for wrong, right in rpswrds.items():
        string = string.replace(wrong,right)
    return string



