import csv
from io import TextIOWrapper

from django.conf import settings
from django.db import models
from django.http import HttpResponse


class Master_assetlist(models.Model):
    name = models.CharField(max_length=128)
    account_number = models.CharField(max_length=24, default='-')
    sequense = models.IntegerField()
    isAsset = models.IntegerField(default=1)
    alive = models.BooleanField(default=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        # 資産の登録時にマスター名+口座番号を表示させる。
        return self.name+self.account_number


class AssetList(models.Model):
    ki = models.IntegerField(default=0)
    account_type = models.CharField(
        choices=settings.ACCOUNTING_TYPE,  max_length=16)
    master = models.ForeignKey(
        Master_assetlist, on_delete=models.PROTECT, null=True, blank=True)
    asset = models.BigIntegerField(default=0)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.master.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ki", "account_type", "master"],
                name="assetlist_unique"
            ),
        ]

    # 以下はcsv入出力のテストのため
    def export_csv():
        """ 資産データをcsvファイルとしてダウンロード """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachement; filename="assetlist.csv"'
        writer = csv.writer(response)
        field = ['id', 'ki', 'account_type', 'master', 'asset', 'comment']
        writer.writerow(field)
        for data in AssetList.objects.all():
            writer.writerow([data.pk, data.ki, data.account_type, data.master,
                            data.asset, data.comment])
        return response

    def import_csv(filename):
        """ 資産データを読み込む """
        form_data = TextIOWrapper(filename, encoding='utf-8')
        csv_file = csv.reader(form_data)

        for line in csv_file:
            asset, created = AssetList.objects.get_or_create(name=line[0])
            asset.ki = line[1]
            asset.account_type = line[2]
            asset.master = Master_assetlist.objects.get(name=line[3])
            asset.asset = line[4]
            asset.comment = line[5]
            asset.save()
        return
