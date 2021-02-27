import logging
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models.aggregates import Case, Sum, When
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views import generic

from kanrihi_in.forms import Kanrihi_incomeForm, Kanrihi_masterForm, Master_categoryForm
from kanrihi_in.models import Kanrihi_income, Master_kanrihi_income, Category_income


class IncomeListView(LoginRequiredMixin, generic.TemplateView):
    """ 管理費収入リスト表示 """
    model = Kanrihi_income
    template_name = "kanrihi_in/income_list.html"  # template名の指定は必須．

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user_id = self.request.user.id
        # sql文を生成する。
        """
        参考url http://thinkami.hatenablog.com/entry/2015/09/04/235841
        行の集約：values().annotate()の順番で記述する．
        values()：集約キー
        annotate()：下記を参照
        問題点：(master_code > 30 AND master_code <100)が使えない？
                (master_code gt 30 AND master_code lt 100)？
        """
        a = Kanrihi_income.objects.select_related().order_by('ki')
        context['incomelist'] = a.values('ki').annotate(
            zenki_kurikosi=Sum(Case(When(master__category__code=10, then='income'), default=0)),
            kanrihi=Sum(
                Case(When(master__category__code=20, then='income'), default=0)),
            sonota=Sum(
                Case(When(master__category__code=30, then='income'), default=0)),
            parking=Sum(
                Case(When(master__category__code=40, then='income'), default=0)),
            total=Sum('income'),
        )
        return context


class UchiwakeListView(LoginRequiredMixin, generic.TemplateView):
    """ その他収入内訳リスト表示 """
    model = Kanrihi_income
    template_name = "kanrihi_in/uchiwake_list.html"  # template名の指定は必須．

    def get_context_data(self, **kwargs):
        # はじめに継承元のメソッドを呼び出す．（おまじない）
        context = super().get_context_data(**kwargs)
        # user_id = self.request.user.id
        # sql文を生成する。
        a = Kanrihi_income.objects.select_related().order_by('ki')
        context['sonotalist'] = a.values('ki').annotate(
            niwa=Sum(Case(When(master__code=40, then='income'), default=0)),
            bike=Sum(Case(When(master__code=50, then='income'), default=0)),
            ryokuchi=Sum(
                Case(When(master__code=60, then='income'), default=0)),
            risoku=Sum(Case(When(master__code=70, then='income'), default=0)),
            zatu=Sum(Case(When(master__code=80, then='income'), default=0)),
            hoken=Sum(Case(When(master__code=90, then='income'), default=0)),
        )
        return context


class CreateIncomeView(PermissionRequiredMixin, generic.CreateView):
    """ 管理費収入データを登録する """
    model = Kanrihi_income
    form_class = Kanrihi_incomeForm
    template_name = "kanrihi_in/kanrihi_income_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy('kanrihi_in:create_income')

    def form_valid(self, form):
        """ 駐車場収入は駐車場会計で処理する """
        kanrihi_data = form.save(commit=False)
        master = form.cleaned_data['master']
        if master != '駐車場収入':
            kanrihi_data.save()
            messages.success(self.request, "保存しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)


class UpdateIncomelistView(PermissionRequiredMixin, generic.ListView):
    """ 修正するデータを選択するための一覧表を表示
        https://docs.djangoproject.com/ja/2.0/topics/pagination/
        http://thinkami.hatenablog.com/entry/2016/02/04/231901
    """
    model = Kanrihi_income
    template_name = 'kanrihi_in/update_list.html'
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    ordering = ['-ki']
    paginate_by = 40


class UpdateIncomeView(PermissionRequiredMixin, generic.UpdateView):
    """ 管理費収入データを修正する """
    model = Kanrihi_income
    form_class = Kanrihi_incomeForm
    template_name = "kanrihi_in/kanrihi_income_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy('kanrihi_in:update_list')

    def form_valid(self, form):
        """ 駐車場収入は駐車場会計で処理する """
        kanrihi_data = form.save(commit=False)
        master = form.cleaned_data['master']
        if master != '駐車場収入':
            kanrihi_data.save()
            messages.success(self.request, "保存しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)


class CreateMasterView(PermissionRequiredMixin, generic.CreateView):
    """ 管理費マスターデータを登録する """
    model = Master_kanrihi_income
    form_class = Kanrihi_masterForm
    template_name = "kanrihi_in/master_income_form.html"
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # マスターデータを表示させるため、get_context_dataをオーバーライド。
    # get_queryset()を上書きしてもよいが、templateに渡すデフォルトの変数を覚えるのが
    # 面倒なため、contextで変数名を自分で設定。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist'] = Master_kanrihi_income.objects.all()
        return context

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('kanrihi_in:create_master')

    # データvalidationが成功したら、メッセージを表示させる。
    def form_valid(self, form):
        messages.success(self.request, "保存しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)


class UpdateMasterView(PermissionRequiredMixin, generic.UpdateView):
    """ 管理費収入項目マスターを修正する """
    model = Master_kanrihi_income
    form_class = Kanrihi_masterForm
    template_name = "kanrihi_in/master_income_form.html"
    permission_required = ("asset_list.add_assetlist")

    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('kanrihi_in:create_master')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist'] = Master_kanrihi_income.objects.all()
        return context


class CreateCategoryView(PermissionRequiredMixin, generic.CreateView):
    """ 管理費収入カテゴリーを登録する """
    model = Category_income
    form_class = Master_categoryForm
    template_name = "kanrihi_in/category_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('kanrihi_in:create_category')

    # データvalidationが成功したら、メッセージを表示させる。
    def form_valid(self, form):
        messages.success(self.request, "保存しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)

    # マスターデータを表示させるため、get_context_dataをオーバーライド。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist'] = Category_income.objects.all().order_by('code')
        return context


class UpdateCategoryView(PermissionRequiredMixin, generic.UpdateView):
    """ 管理費支出カテゴリーを修正する """
    model = Category_income
    form_class = Master_categoryForm
    template_name = "kanrihi_in/category_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('kanrihi_in:create_category')

    # マスターデータを表示させるため、get_context_dataをオーバーライド。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist'] = Category_income.objects.all()
        return context
