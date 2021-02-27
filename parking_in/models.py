from django.db import models


class Master_parking_income(models.Model):
    """ 駐車場収入マスター項目 """
    code = models.IntegerField()
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Parking_income(models.Model):
    ki = models.IntegerField(unique=True)
    master = models.ForeignKey(Master_parking_income, on_delete=models.PROTECT, null=True)
    parking_lot_income = models.BigIntegerField(default=0)

    def __int__(self):
        return self.parking_lot_income
