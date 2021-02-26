from django.db import models


class Parking_income(models.Model):
    ki = models.IntegerField(unique=True)
    parking_lot_income = models.BigIntegerField(default=0)

    def __int__(self):
        return self.parking_lot_income
