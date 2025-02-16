from django.core.management.base import BaseCommand
from dataCollect.models import partList
from dataCollect.crawler.data_p1_cp import coolpc
from dataCollect.crawler.data_p1_nt import newton
from dataCollect.dataParser import analysis
from dataCollect.models import autoupdateLog
from datetime import datetime
import pytz

class Command(BaseCommand):
    help = "crawling data from computer store wesites and update the database"

    def add_arguments(self, parser):
        parser.add_argument("--update", type=str, help="要更新資料的店家")
        parser.add_argument("--test", type=str, help="功能測試")

    def coolpc_update(self):
        chart = coolpc()
        chartDict = chart.to_dict(orient="records")
        partList.objects.bulk_create([partList(**temp) for temp in chartDict])
    
    def newton_update(self):
        chart = newton()
        chartDict = chart.to_dict(orient="records")
        partList.objects.bulk_create([partList(**temp) for temp in chartDict])  

    def data_parse(self):
        print("Start spec parsing")
        parsedData = analysis()
        for rowNum, data in parsedData.iterrows():
            dbData = partList.objects.get(id=data["id"])
            dbData.brand = data["brand"]
            dbData.spec1 = data["spec1"]
            dbData.unit1 = data["unit1"]
            dbData.spec2 = data["spec2"]
            dbData.unit2 = data["unit2"]
            dbData.spec3 = data["spec3"]
            dbData.unit3 = data["unit3"]
            dbData.spec4 = data["spec4"]
            dbData.unit4 = data["unit4"]
            dbData.save()
        result = "Parsed data saved"
        return result
    
    def data_clean(self):
        print("----- NG data deleting ")
        db_Data = partList.objects.all()
        for i in db_Data:
            if i.brand == "NG" or i.spec1 == "NG" or i.spec2 == "NG" or i.spec3 == "NG" or i.spec4 == "NG":
                i.delete()
        result = "----- Data ready"
        return result        


    def handle(self, **options):

        if options["test"] == "crawling":
            partList.objects.all().delete()
            self.coolpc_update()
            print("----- coolpc crawling DONE ")
            self.newton_update()        
            print("----- newton crawling DONE ")

        elif options["test"] == "parsing":
            
            result = self.data_parse()
            print(result)
            result = self.data_clean()
            print(result)

        elif options["update"] == "all":
            partList.objects.all().delete()
            self.coolpc_update()
            print("----- coolpc crawling DONE ")
            self.newton_update()        
            print("----- newton crawling DONE ")
            result = self.data_parse()
            print(result)
            result = self.data_clean()
            print(result)
        
        elif options["update"] == "auto":
            # 處理日期時間
            tz = pytz.timezone("Asia/Taipei")
            date_time = datetime.now(tz)
            weekday = date_time.date().weekday() # 0 = 週一, 1 = 週二 ...
            # 資料更新
            if weekday == 2 or weekday == 7:
                partList.objects.all().delete()
                try:
                    self.coolpc_update()
                    coolpcUpdate = "Success"
                except:
                    coolpcUpdate = "Failed"
                try:
                    self.newton_update()
                    newtonUpdate = "Success"
                except:
                    newtonUpdate = "Failed"
                try:
                    self.data_parse()
                    dataParse = "Success"
                except:
                    dataParse = "Failed"
                try:
                    result = self.data_clean()
                    dataClean = "Success"
                except:
                    dataClean = "Failed"
            else:
                coolpcUpdate = "--------"
                newtonUpdate = "--------"
                dataParse = "--------"
                dataClean = "--------"
            # result and saving log
            if coolpcUpdate == "Success" and newtonUpdate == "Success" and dataParse == "Success" and dataClean == "Success":
                updateResult = "Update Done"
            elif coolpcUpdate == "--------" and newtonUpdate == "--------" and dataParse == "--------" and dataClean == "--------":
                updateResult = "--------"
            else:
                updateResult = "Failed"
            result = {"dateTime":date_time,"weekDay":weekday,"coolpcUpdate":coolpcUpdate,"newtonUpdate":newtonUpdate,
                      "dataParse":dataParse,"dataClean":dataClean,"updateResult":updateResult}
            for i in result:
                print(f"{i}:"+str(result[i]))
            autoupdateLog.objects.create(dateTime=date_time,weekDay=weekday,coolpcUpdate=coolpcUpdate,newtonUpdate=newtonUpdate,
                                         dataParse=dataParse,dataClean=dataClean,updateResult=updateResult)
        else:
            print("ERR")