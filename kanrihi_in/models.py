from django.db import models


class Category_income(models.Model):
    """ 2019-01-06追加 """
    code = models.IntegerField()
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Master_kanrihi_income(models.Model):
    """ 管理費収入の項目を定義 """
    code = models.IntegerField()
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category_income, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class Kanrihi_income(models.Model):
    ki = models.IntegerField()
    master = models.ForeignKey(Master_kanrihi_income, on_delete=models.PROTECT, null=True)
    income = models.BigIntegerField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.master.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ki", "master"],
                name="kanrihi_in_unique"
            ),
        ]

    """
    https://stackoverflow.com/questions/9297422/get-or-create-failure
    -with-django-and-postgres-duplicate-key-value-violates-uni
    postgrSQLの場合、csvファイルからの読み込みでは以下の設定が必要のようだ。
    unique制約を追加。https://torina.top/detail/298/

    class Meta:
        select_on_save = True
        unique_together = ('ki','master')
    """
