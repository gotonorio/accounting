# Create your models here.
from django.db import models
from django.conf import settings
from asset_list.models import AccountType


class Master_koujitype(models.Model):
    """ 修繕計画における工事区分 """
    koujitype = models.CharField(max_length=256)
    sequense = models.IntegerField()
    live = models.IntegerField(default=1)  # 0 or 1

    def __str__(self):
        return self.koujitype


class Constractor(models.Model):
    """ 施工業者 """
    sequense = models.IntegerField(default=0)
    name = models.CharField(max_length=128, unique=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Shuuzenhi_expense(models.Model):
    """ 工事支出データ """
    year = models.IntegerField(default=2009)
    # month = models.IntegerField(null=True, blank=True)
    # django2ではon_deleteが無いとエラー．https://code.i-harness.com/ja/q/59f5a4
    koujitype = models.ForeignKey(Master_koujitype, on_delete=models.PROTECT, null=True)
    koujimei = models.CharField(max_length=256)
    cost = models.BigIntegerField()
    constractor = models.ForeignKey(Constractor, on_delete=models.PROTECT, null=True, blank=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT, null=True, blank=True)
    # 見積書ファイルデータのID
    quotation_id = models.IntegerField(default=0)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.koujimei

    # costの合計をpython関数で求める。
    def calc_total(self, sql):
        cost_list = sql
        total = 0
        for data in cost_list:
            total += data.cost
        return total
