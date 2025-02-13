from django.db import models

# Create your models here.

class partList(models.Model):
    id = models.AutoField(primary_key=True)
    store = models.CharField(max_length=8, blank=True)
    category = models.CharField(max_length=16, blank=True)
    sub_cate = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=256, blank=True)
    brand = models.CharField(max_length=32, blank=True)
    spec1 = models.CharField(max_length=32, blank=True)
    unit1 = models.CharField(max_length=8, blank=True)
    spec2 = models.CharField(max_length=32, blank=True)
    unit2 = models.CharField(max_length=8, blank=True)
    spec3 = models.CharField(max_length=32, blank=True)
    unit3 = models.CharField(max_length=8, blank=True)
    spec4 = models.CharField(max_length=32, blank=True)
    unit4 = models.CharField(max_length=8, blank=True)
    orgPrice = models.IntegerField(blank=True, null=True)
    saleEnd = models.DateField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}/{self.category}/{self.brand}/{self.spec1}/{self.spec2}/{self.spec3}/{self.spec4}"

class autoupdateLog(models.Model):
    id = models.AutoField(primary_key=True)
    dateTime = models.DateTimeField(blank=True, null=True)
    weekDay = models.IntegerField(default=8) # 預設值設為 8，若log資料表中出現 weekDay 這欄是 8，代表沒有填資料進去
    coolpcUpdate = models.CharField(max_length=8, blank=True)
    newtonUpdate = models.CharField(max_length=8, blank=True)
    dataParse = models.CharField(max_length=8, blank=True)
    dataClean = models.CharField(max_length=8, blank=True)
    updateResult = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return f"{self.id} - {self.datetime} - {self.updateResult}"