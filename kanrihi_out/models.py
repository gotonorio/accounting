from django.db import models


class Master_category(models.Model):
    """ 管理費支出のカテゴリーを定義。
        定額管理費 設備管理業務費 消費税 共用部分直接費
    """
    code = models.IntegerField(default=0)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Master_expense(models.Model):
    """ 管理費支出の項目を定義。 """
    code = models.IntegerField(default=0)
    sequense = models.IntegerField()
    name = models.CharField(max_length=256)
    category = models.ForeignKey(
        Master_category, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name


class Kanrihi_expense(models.Model):
    """ 管理費支出データ。
        CSVデータ構造 : id(pk),ki,master（外部制約）,expense,user（外部制約）
    """
    ki = models.IntegerField()
    # django2ではon_deleteが無いとエラー
    master = models.ForeignKey(
        Master_expense, on_delete=models.PROTECT, null=True, blank=True)
    expense = models.BigIntegerField()

    def __str__(self):
        return self.master.name
