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
        """ ユニーク制約の設定
        https://docs.djangoproject.com/en/3.1/ref/models/options/#django.db.models.Options.unique_together
        """
        constraints = [
            models.UniqueConstraint(
                fields=["ki", "master"],
                name="kanrihi_in_unique"
            ),
        ]
