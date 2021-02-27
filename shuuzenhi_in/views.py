# import logging
from django.contrib import messages  # メッセージフレームワーク
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models.aggregates import Case, Sum, When
from django.shortcuts import reverse
from django.views import generic

from shuuzenhi_in.forms import Shuuzenhi_incomeForm, Shuuzenhi_masterForm
from shuuzenhi_in.models import Master_shuuzenhi_income, Shuuzenhi_income


class IncomeListView(LoginRequiredMixin, generic.TemplateView):
    """ 修繕費収入履歴 """
    model = Shuuzenhi_income
    template_name = "shuuzenhi_in/income_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user_id = self.request.user.id
        a = Shuuzenhi_income.objects.select_related().order_by('ki')
        context['incomelist'] = a.values('ki').annotate(
            zenki=Sum(Case(When(master__code=10, then='income'), default=0)),
            shuuzenhi=Sum(
                Case(When(master__code=20, then='income'), default=0)),
            niwa=Sum(Case(When(master__code=25, then='income'), default=0)),
            bike=Sum(Case(When(master__code=30, then='income'), default=0)),
            motor_bike=Sum(Case(When(master__code=35, then='income'), default=0)),
            risoku=Sum(Case(When(master__code=40, then='income'), default=0)),
            parking=Sum(Case(When(master__code=50, then='income'), default=0)),
            zatu=Sum(Case(When(master__code=60, then='income'), default=0)),
            kuriire=Sum(Case(When(master__code=70, then='income'), default=0)),
            haitou=Sum(Case(When(master__code=80, then='income'), default=0)),
            total=Sum('income'),
        )
        return context


class CreateIncomeView(PermissionRequiredMixin, generic.CreateView):
    """ 修繕費収入データの登録
    何かの役に立つかも知れないform_valid()に関する情報。
    http://k-mawa.hateblo.jp/entry/2017/10/20/181711
    """
    model = Shuuzenhi_income
    form_class = Shuuzenhi_incomeForm
    template_name = "shuuzenhi_in/shuuzenhi_income_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl。プロパティ(seccess_url)を使うか、関数をオーバーライド。
    def get_success_url(self):
        return reverse('shuuzenhi_in:create')

    def form_valid(self, form):
        """ 駐車場収入は駐車場会計で処理する """
        shuuzenhi_data = form.save(commit=False)
        master = form.cleaned_data['master']
        if master != '駐車場収入':
            shuuzenhi_data.save()
            messages.success(self.request, "保存しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)


class UpdateIncomeView(PermissionRequiredMixin, generic.UpdateView):
    """ 修繕費収入データを修正する """
    model = Shuuzenhi_income
    form_class = Shuuzenhi_incomeForm
    template_name = "shuuzenhi_in/shuuzenhi_income_form.html"
    # 必要な権限（データ登録できる権限は共通）
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('shuuzenhi_in:update_list')

    def form_valid(self, form):
        """ 駐車場収入は駐車場会計で処理する """
        shuuzenhi_data = form.save(commit=False)
        master = form.cleaned_data['master']
        if master != '駐車場収入':
            shuuzenhi_data.save()
            messages.success(self.request, "保存しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)


class CreateMasterView(PermissionRequiredMixin, generic.CreateView):
    """ 修繕費収入項目マスターを作成する """
    model = Master_shuuzenhi_income
    form_class = Shuuzenhi_masterForm
    template_name = "shuuzenhi_in/master_shuuzenhi_income_form.html"

    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl。プロパティ(seccess_url)を使うか、関数をオーバーライド。
    def get_success_url(self):
        return reverse('shuuzenhi_in:create_master')

    # マスターデータを表示させるため、get_context_dataをオーバーライド。
    # get_queryset()を上書きしてもよいが、templateに渡すデフォルトの変数を覚えるのが
    # 面倒なため、contextで変数名を自分で設定。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist'] = Master_shuuzenhi_income.objects.all().order_by("code")
        return context


class UpdateMasterView(PermissionRequiredMixin, generic.UpdateView):
    """ 修繕費収入項目マスターを修正する """
    model = Master_shuuzenhi_income
    form_class = Shuuzenhi_masterForm
    template_name = "shuuzenhi_in/master_shuuzenhi_income_form.html"
    permission_required = ("asset_list.add_assetlist")

    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('shuuzenhi_in:create_master')

    # マスターデータを表示させるため、get_context_dataをオーバーライド。
    # get_queryset()を上書きしてもよいが、templateに渡すデフォルトの変数を覚えるのが
    # 面倒なため、contextで変数名を自分で設定。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist'] = Master_shuuzenhi_income.objects.all().order_by("code")
        return context


class DatalistView(PermissionRequiredMixin, generic.ListView):
    """ 修繕費収入データ修正用listを表示
    https://docs.djangoproject.com/ja/2.0/topics/pagination/
    http://thinkami.hatenablog.com/entry/2016/02/04/231901
    """
    model = Shuuzenhi_income
    template_name = 'shuuzenhi_in/update_list.html'
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    ordering = ['-ki']
    paginate_by = 50
