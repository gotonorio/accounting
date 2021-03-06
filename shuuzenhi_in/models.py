from django.db import models


class Category_shuuzenhi_income(models.Model):
    """ 2021-03-10追加 """
    code = models.IntegerField()
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Master_shuuzenhi_income(models.Model):
    """ 修繕費収入の項目を定義。 """
    code = models.IntegerField()
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category_shuuzenhi_income, on_delete=models.PROTECT, null=True)
    alive = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.name
    """
    https://stackoverflow.com/questions/9297422/get-or-create-failure-with-django-and-postgres-duplicate-key-value-violates-uni
    postgrSQL,MySQLの場合、csvファイルからの読み込みでは以下の設定が必要のようだ。
    class Meta:
        select_on_save = True
        unique_together = ('code', 'name')
    """


class Shuuzenhi_income(models.Model):
    ki = models.IntegerField()
    master = models.ForeignKey(Master_shuuzenhi_income, on_delete=models.PROTECT)
    income = models.BigIntegerField()
    comment = models.TextField(null=True, blank=True)

    def __int__(self):
        return self.income

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ki", "master"],
                name="shuuzenhi_in_unique"
            ),
        ]
