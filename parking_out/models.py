from django.conf import settings
from django.db import models
# import logging


class Parking_expenditure(models.Model):
    """ 駐車場収入の支出リスト """
    ki = models.IntegerField()
    account_type = models.CharField(
        choices=settings.ACCOUNTING_TYPE,  max_length=16)
    koujimei = models.CharField(max_length=256, default='')
    cost = models.BigIntegerField(default=0)
    comment = models.TextField(blank=True, null=True)

    def __int__(self):
        return self.cost

    # costの合計を計算。
    def calc_total(self, sql):
        kanrihi_total = 0
        shuuzenhi_total = 0
        for data in sql:
            kanrihi_total += data['kanrihi']
            shuuzenhi_total += data['shuuzenhi']
        return kanrihi_total, shuuzenhi_total

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ki", "account_type"],
                name="parking_out_unique"
            ),
        ]
