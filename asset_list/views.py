import csv
import logging

from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models.aggregates import Case, Max, Sum, When
from django.http import HttpResponse
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views import generic

from asset_list.forms import AssetListForm, BalanceSheetForm, Master_assetForm
from asset_list.lib import append_list
from asset_list.models import AssetList, Master_assetlist


class AssetListView(LoginRequiredMixin, generic.TemplateView):
    """ 資産データを表示する。 """
    model = AssetList
    template_name = "asset_list/assetlist.html"

    def get_context_data(self, **kwargs):
        # はじめに継承元のメソッドを呼び出す。
        context = super().get_context_data(**kwargs)
        # ボタンを読み込む。
        button = self.request.GET.get('button')
        # sessionデータを確認して、sessionデータがあれば読み込む。
        if 'assetlist_maxki' in self.request.session:
            ki = self.request.session['assetlist_maxki']
        else:   # sessionデータが存在しない場合。
            qs = AssetList.objects.all().aggregate(Max('ki'))
            if qs["ki__max"] is None:
                ki = 0
            else:
                ki = qs['ki__max']
        maxki = int(ki)
        if button == 'forward':
            maxki = maxki-1
        elif button == 'next':
            maxki = maxki+1
        if maxki < 6:
            maxki = 5
        # sessionに表示されている最大期を保存する。
        self.request.session['assetlist_maxki'] = maxki
        # logging.debug(maxki)
        context['title1'] = str(maxki-4)+"期"
        context['title2'] = str(maxki-3)+"期"
        context['title3'] = str(maxki-2)+"期"
        context['title4'] = str(maxki-1)+"期"
        context['title5'] = str(maxki)+"期"
        # 資産
        obj = AssetList.objects
        # Master_assetlistのorder順で出力させる。
        a = obj.select_related()
        a = a.filter(master__isAsset=1).order_by('master__sequense')
        # valuesには抽出対象の列名を記述。
        context['assetlist'] = a.values(
            'master__name', 'master__account_number').annotate(
            period1=Sum(Case(When(ki=maxki-4, then='asset'), default=0)),
            period2=Sum(Case(When(ki=maxki-3, then='asset'), default=0)),
            period3=Sum(Case(When(ki=maxki-2, then='asset'), default=0)),
            period4=Sum(Case(When(ki=maxki-1, then='asset'), default=0)),
            period5=Sum(Case(When(ki=maxki, then='asset'), default=0)),
        )
        # 資産合計を求める
        context['total1'] = obj.filter(
            ki=maxki-4, master__isAsset=1).aggregate(Sum('asset'))['asset__sum']
        context['total2'] = obj.filter(
            ki=maxki-3, master__isAsset=1).aggregate(Sum('asset'))['asset__sum']
        context['total3'] = obj.filter(
            ki=maxki-2, master__isAsset=1).aggregate(Sum('asset'))['asset__sum']
        context['total4'] = obj.filter(
            ki=maxki-1, master__isAsset=1).aggregate(Sum('asset'))['asset__sum']
        context['total5'] = obj.filter(
            ki=maxki, master__isAsset=1).aggregate(Sum('asset'))['asset__sum']
        # 負債
        b = obj.select_related().filter(
            master__isAsset=0).order_by('master__sequense')
        # valuesには抽出対象の列名を記述。
        context['debtlist'] = b.values(
            'master__name', 'master__account_number').annotate(
                period1=Sum(Case(When(ki=maxki-4, then='asset'), default=0)),
                period2=Sum(Case(When(ki=maxki-3, then='asset'), default=0)),
                period3=Sum(Case(When(ki=maxki-2, then='asset'), default=0)),
                period4=Sum(Case(When(ki=maxki-1, then='asset'), default=0)),
                period5=Sum(Case(When(ki=maxki, then='asset'), default=0)),
        )
        # 負債合計を求める
        context['debt1'] = obj.filter(
            ki=maxki-4, master__isAsset=0).aggregate(Sum('asset'))['asset__sum']
        context['debt2'] = obj.filter(
            ki=maxki-3, master__isAsset=0).aggregate(Sum('asset'))['asset__sum']
        context['debt3'] = obj.filter(
            ki=maxki-2, master__isAsset=0).aggregate(Sum('asset'))['asset__sum']
        context['debt4'] = obj.filter(
            ki=maxki-1, master__isAsset=0).aggregate(Sum('asset'))['asset__sum']
        context['debt5'] = obj.filter(ki=maxki, master__isAsset=0).aggregate(
            Sum('asset'))['asset__sum']
        # 資産グラフデータ
        c = obj.select_related().order_by('ki')
        asset_graphdata = c.values('ki').annotate(
            asset=Sum(Case(When(master__isAsset=1, then='asset'), default=0)))
        # 負債グラフデータ
        d = obj.select_related().order_by('ki')
        debt_graphdata = d.values('ki').annotate(
            debt=Sum(Case(When(master__isAsset=0, then='asset'),default=0)))
        # 正味資産データ
        data = []
        for asset, debt in zip(asset_graphdata, debt_graphdata):
            ki = []
            if asset:
                ki.append(asset['ki'])
                ki.append(asset['asset'] - debt['debt'])
                data.append(ki)
        context['graphdata'] = data
        return context


class CreateAssetView(PermissionRequiredMixin, generic.CreateView):
    """ 資産データを登録する
        自動的にform変数を作成してテンプレートに渡す。
        http://k-mawa.hateblo.jp/entry/2017/10/20/181711
        管理者権限を持つユーザーのみが使用可能とする。
        https://torina.top/detail/295/
    """
    model = AssetList
    form_class = AssetListForm
    template_name = "asset_list/assetlist_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    # 保存が成功した場合に遷移するurl。特に何か処理しないのであれば、
    success_url = reverse_lazy('asset_list:create')

    def form_valid(self, form):
        """ 失敗した時だけメッセージを表示 """
        messages.success(self.request, "保存しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)


class UpdateAssetView(PermissionRequiredMixin, generic.UpdateView):
    """ 資産データを修正する """
    model = AssetList
    form_class = AssetListForm
    template_name = "asset_list/assetlist_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    def get_success_url(self):
        """ 保存が成功した場合に遷移するurl """
        return reverse('asset_list:update_list')


class UpdateAssetlistView(PermissionRequiredMixin, generic.ListView):
    """ 修正するデータを選択するための一覧表を表示 """
    model = AssetList
    template_name = 'asset_list/update_list.html'
    # 必要な権限(一つの権限を使い回す)
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    ordering = ['-ki', 'master__sequense']
    paginate_by = 50


class CreateMasterView(PermissionRequiredMixin, generic.CreateView):
    """ 資産マスターを登録する """
    model = Master_assetlist
    form_class = Master_assetForm
    template_name = "asset_list/master_assetlist_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    def get_success_url(self):
        """ 保存が成功したら遷移するurl """
        return reverse('asset_list:create_master')

    # データvalidationが成功したら、直ぐにコミットせず、メッセージを表示させる。
    # 以下はuserを入力させずに、既定値を登録する例として残す。
    def form_valid(self, form):
        messages.success(self.request, "保存しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist'] = Master_assetlist.objects.all().order_by('sequense')
        return context


class UpdateMasterView(PermissionRequiredMixin, generic.UpdateView):
    """ 資産マスターを修正する """
    model = Master_assetlist
    form_class = Master_assetForm
    template_name = "asset_list/master_assetlist_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    def get_success_url(self):
        return reverse('asset_list:create_master')

def asset_export(request):
    """ 資産データをCSVで出力する
    https://torina.top/detail/324/#i3-2
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="asset_data.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    writer.writerow(["期", "項目名", "資産金額"])
    for i in AssetList.objects.all():
        writer.writerow([i.ki, i.master, i.asset])
    return response


class BalanceSheetView(LoginRequiredMixin, generic.TemplateView):
    """ 貸借対照表を表示する。 """
    model = AssetList
    form_class = BalanceSheetForm
    template_name = "asset_list/balancesheet.html"

    @staticmethod
    def make_balancesheet(asset, debt):
        """ 資産リストと負債リストから貸借対照表を生成する。
        配列を結合するためにnumpyのinsertを利用してみる。
        """
        asset_list = []
        asset_total = 0
        debt_list = []
        debt_total = 0
        # 資産リストを作成
        for item in asset:
            row_list = []
            row_list.append(item.master)
            row_list.append(item.asset)
            asset_list.append(row_list)
            asset_total += int(item.asset)
        # 負債リストを作成
        for item in debt:
            row_list = []
            row_list.append(item.master)
            row_list.append(item.asset)
            debt_list.append(row_list)
            debt_total += item.asset
        # 資本金（次期繰越）の行を追加。
        debt_list.append(['次期繰越金', asset_total-debt_total])
        # template表示用に「資産リスト」「負債リスト」をまとめる。
        c = append_list.append_list(asset_list, debt_list, '')
        return c, asset_total

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asset_total = 0
        asset2_total = 0
        ki = self.request.GET.get('ki')
        if ki is None:
            max_ki = AssetList.objects.aggregate(ki=Max('ki'))
            ki = max_ki["ki"]

        # 管理費会計 資産の部
        bs = AssetList.objects.filter(ki=ki)
        bs_asset = bs.filter(master__isAsset=1, account_type='管理費会計')
        bs_asset = bs_asset.order_by('master__sequense')
        # 管理費会計 負債の部
        bs_debt = bs.filter(master__isAsset=0, account_type='管理費会計')
        bs_debt = bs_debt.order_by('master__sequense')
        # データの不備に対応するための一時的な処理。
        if len(bs_asset) > 0:
            bs, asset_total = self.make_balancesheet(bs_asset, bs_debt)

        # 修繕費会計 資産の部
        bs2 = AssetList.objects.filter(ki=ki)
        bs2_asset = bs2.filter(master__isAsset=1, account_type='修繕費会計')
        bs2_asset = bs2_asset.order_by('master__sequense')
        # 修繕費会計 負債の部
        bs2_debt = bs2.filter(master__isAsset=0, account_type='修繕費会計')
        bs2_debt = bs2_debt.order_by('master__sequense')
        # データの不備に対応するための一時的な処理。
        if len(bs2_asset) > 0:
            bs2, asset2_total = self.make_balancesheet(bs2_asset, bs2_debt)

        # formフィールドに初期値を設定。
        balancesheetform = BalanceSheetForm(initial={
            'ki': ki,
        })
        context['ki'] = ki
        context['balancesheet'] = bs
        context['asset_total'] = asset_total
        context['balancesheet2'] = bs2
        context['asset_total2'] = asset2_total
        context['form'] = balancesheetform
        return context
