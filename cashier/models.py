from django.db import models
from django.utils import timezone


class ExpenseItem(models.Model):
    """ 費目 """
    item = models.CharField('費目名', max_length=32, default='none')

    def __str__(self):
        return self.item


class Account_subject(models.Model):
    """ 消耗品等小口会計 """
    spending_date = models.DateField('日付', default=timezone.datetime.today)
    name = models.CharField('項目名', max_length=64)
    expense_item = models.ForeignKey(ExpenseItem, on_delete=models.PROTECT, null=True)
    expense = models.IntegerField('支出額')
    comment = models.TextField('摘要')

    def __str__(self):
        return self.name
