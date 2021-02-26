# import logging

from django.contrib import messages  # メッセージフレームワーク
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models.aggregates import Case, Sum, When
from django.shortcuts import reverse
from django.views import generic

from kanrihi_in.models import Kanrihi_income
from parking_out.forms import Parking_expenditureForm
from parking_out.models import Parking_expenditure
from shuuzenhi_in.models import Shuuzenhi_income


class ExpenditureListView(LoginRequiredMixin, generic.TemplateView):
    """ 駐車場使用料支出リスト一覧 """
    model = Parking_expenditure
    template_name = "parking_out/expend_list.html"

    def parking_expense(self):
        a = Parking_expenditure.objects.select_related().order_by('ki')
        expenselist = a.values('ki').annotate(
            kanrihi=Sum(
                Case(When(account_type='管理費会計', then='cost'), default=0)),
            shuuzenhi=Sum(
                Case(When(account_type='修繕費会計', then='cost'), default=0)),
            total=Sum(Case(
                When(account_type='管理費会計', then='cost'),
                When(account_type='修繕費会計', then='cost'),
                default=0
            ))
        )
        return expenselist

    def get_context_data(self, **kwargs):
        """ 最初に画面表示された時は、account_typeはFalse。
        表示ボタンが押された時には、選択されたac_typeが取得できる。
        """
        context = super().get_context_data(**kwargs)
        ac_type = self.request.GET.get('account_type', False)
        # queryの作成。
        qs = Parking_expenditure.objects
        if ac_type:
            qs = qs.filter(account_type=ac_type).order_by('ki')
        else:
            qs = Parking_expenditure.objects.order_by('ki')

        qs = self.parking_expense()
        kanrihi_total, shuuzenhi_total = Parking_expenditure.calc_total(self, qs)

        context['expendlist'] = qs
        context['kanrihi_total'] = kanrihi_total
        context['shuuzenhi_total'] = shuuzenhi_total
        return context


class ExpenditureCreateView(PermissionRequiredMixin, generic.CreateView):
    """ 駐車場使用料支出データの登録
        自動的にform変数を作成してテンプレートに渡す。
        http://k-mawa.hateblo.jp/entry/2017/10/20/181711
        管理者権限を持つユーザーのみが使用可能とする。（パーミッション機能）
        https://torina.top/detail/295/
    """
    model = Parking_expenditure
    form_class = Parking_expenditureForm
    template_name = "parking_out/parking_expenditure_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl。プロパティ(seccess_url)を使うか、関数をオーバーライド。
    def get_success_url(self):
        return reverse('parking_out:create')


class UpdateListView(PermissionRequiredMixin, generic.ListView):
    """ 駐車場使用料支出データ修正用listを表示
        https://docs.djangoproject.com/ja/2.0/topics/pagination/
        http://thinkami.hatenablog.com/entry/2016/02/04/231901
    """
    model = Parking_expenditure
    template_name = 'parking_out/update_list.html'
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    ordering = ['-ki', 'account_type']
    paginate_by = 50


class UpdateExpenditureView(PermissionRequiredMixin, generic.UpdateView):
    """ 駐車場使用料支出データを修正する """
    model = Parking_expenditure
    form_class = Parking_expenditureForm
    template_name = "parking_out/parking_expenditure_form.html"
    # 必要な権限（データ登録できる権限は共通）
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('parking_out:update_list')

    def form_valid(self, form):
        """ 「管理会計収入」「修繕会計収入」のデータがあればアップデートする。
        master_idを決め打ちしているので、マスターデータを変更した場合に注意する。
        2020-09-15 by N.goto
        """
        ki = form.cleaned_data['ki']
        ac_type = form.cleaned_data['account_type']
        cost = form.cleaned_data['cost']
        msg = ''
        if str(ac_type) == '管理費会計':
            # アップデートするオブジェクトを取得。無ければスルー。
            try:
                obj = Kanrihi_income.objects.get(ki=ki, master_id=3)
                obj.income = cost
                obj.save()
            except Kanrihi_income.DoesNotExist:
                pass
            msg = f'管理会計の第{ki}期の駐車場収入もアップデートしました'
        elif str(ac_type) == '修繕費会計':
            # アップデートするオブジェクトを取得。無ければスルー。
            try:
                obj = Shuuzenhi_income.objects.get(ki=ki, master_id=5)
                obj.income = cost
                obj.save()
            except Shuuzenhi_income.DoesNotExist:
                pass
            msg = f'修繕会計の第{ki}期の駐車場収入もアップデートしました'

        messages.info(self.request, msg)
        return super().form_valid(form)
