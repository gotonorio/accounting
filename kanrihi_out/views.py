# import logging

from django.conf import settings
from django.contrib import messages  # メッセージフレームワーク
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models.aggregates import Case, Max, Sum, When
from django.shortcuts import reverse
from django.views import generic
from kanrihi_out.forms import (Kanrihi_expenseForm, Master_categoryForm,
                               Master_expenseForm)
from kanrihi_out.models import Kanrihi_expense, Master_category, Master_expense
from shuuzenhi_in.models import Shuuzenhi_income


class KanrihiExpenseListView(LoginRequiredMixin, generic.TemplateView):
    """ 管理費支出一覧 """
    model = Kanrihi_expense
    template_name = "kanrihi_out/expense_list.html"  # template名の指定は必須．

    def kanrihi_expense(self):
        """ Extract administrative expenses expenditure data
        別アプリ（kanrihi_in）で呼び出すため、独立した関数とする。
        http://thinkami.hatenablog.com/entry/2015/09/04/235841
        行の集約：values().annotate()の順番で記述する．
        支出合計には保険支出及び修繕費会計への支出分は含めない。2021/02/15
        """
        a = Kanrihi_expense.objects.select_related().order_by('ki')
        expenselist = a.values('ki').annotate(
            teigaku=Sum(
                Case(When(master__category__code=10, then='expense'), default=0)),
            setubi=Sum(
                Case(When(master__category__code=20, then='expense'), default=0)),
            tax=Sum(Case(When(master__category__code=30, then='expense'), default=0)),
            chokusetu=Sum(
                Case(When(master__category__code=40, then='expense'), default=0)),
            hoken=Sum(
                Case(When(master__category__code=50, then='expense'), default=0)),
            to_shuuzen=Sum(
                Case(When(master__category__code=99, then='expense'), default=0)),
            out_total=Sum(Case(
                When(master__category__code=10, then='expense'),
                When(master__category__code=20, then='expense'),
                When(master__category__code=30, then='expense'),
                When(master__category__code=40, then='expense'),
                # When(master__category__code=50, then='expense'),
                # When(master__category__code=99, then='expense'),
                default=0
            ))
        )
        return expenselist

    def get_context_data(self, **kwargs):
        """ GETで呼ばれた時に管理費支出一覧を表示する。 """
        context = super().get_context_data(**kwargs)
        context['expenselist'] = self.kanrihi_expense()
        context['start_year'] = settings.START_YEAR
        context['floor_space'] = settings.FLOOR_SPACE
        return context


class BreakdownListView(LoginRequiredMixin, generic.TemplateView):
    """ 管理費支出内訳
        http://python.zombie-hunting-club.com/entry/2017/11/06/222409
    """
    model = Kanrihi_expense
    template_name = "kanrihi_out/breakdown_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # userはここで明示しなくてもtemplateで使用できる？
        context['user'] = self.request.user
        # ボタンを読み込む。
        button = self.request.GET.get('button')
        # sessionデータを確認して、sessionデータがあれば読み込む。
        if 'maxki' in self.request.session:
            ki = self.request.session['maxki']
        else:   # sessionデータが存在しない場合。
            qs = Kanrihi_expense.objects.all().aggregate(Max('ki'))
            if qs["ki__max"] is None:
                ki = 1
            else:
                ki = qs['ki__max']
        maxki = int(ki)
        if maxki < 7:
            maxki = 7
        if button == 'forward':
            maxki = maxki-1
        elif button == 'next':
            maxki = maxki+1
        # sessionに表示されている最大期を保存する。
        self.request.session['maxki'] = maxki
        # logging.debug(maxki)
        context['title1'] = str(maxki-5)+"期"
        context['title2'] = str(maxki-4)+"期"
        context['title3'] = str(maxki-3)+"期"
        context['title4'] = str(maxki-2)+"期"
        context['title5'] = str(maxki-1)+"期"
        context['title6'] = str(maxki)+"期"
        a = Kanrihi_expense.objects.select_related().order_by('master__sequense')
        # 行の集約（valuesには集約キーを指定）
        # http://thinkami.hatenablog.com/entry/2015/09/04/235841
        context['expenseitem'] = a.values(
            'master__id', 'master__category__name', 'master__name').annotate(
                period1=Sum(Case(When(ki=maxki-5, then='expense'), default=0)),
                period2=Sum(Case(When(ki=maxki-4, then='expense'), default=0)),
                period3=Sum(Case(When(ki=maxki-3, then='expense'), default=0)),
                period4=Sum(Case(When(ki=maxki-2, then='expense'), default=0)),
                period5=Sum(Case(When(ki=maxki-1, then='expense'), default=0)),
                period6=Sum(Case(When(ki=maxki, then='expense'), default=0)),
            )
        return context


class CreateMasterView(PermissionRequiredMixin, generic.CreateView):
    """ 管理費支出項目を登録する
        listでページングする場合は https://torina.top/detail/337/#i3 を参照。
    """
    model = Master_expense
    form_class = Master_expenseForm
    template_name = "kanrihi_out/master_expense_form.html"
    # 必要な権限
    permission_required = ("admin.add_logentry")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('kanrihi_out:create_master')

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
        context['masterlist'] = Master_expense.objects.all().order_by('sequense')
        return context


class UpdateMasterView(PermissionRequiredMixin, generic.UpdateView):
    """ 管理費支出項目を修正する """
    model = Master_expense
    form_class = Master_expenseForm
    template_name = "kanrihi_out/master_expense_form.html"
    #template_name = "kanrihi_out/create_master.html"
    # 必要な権限
    permission_required = ("admin.add_logentry")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('kanrihi_out:create_master')

    # マスターデータを表示させるため、get_context_dataをオーバーライド。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist'] = Master_expense.objects.all().order_by('sequense')
        return context


class CreateExpenseView(PermissionRequiredMixin, generic.CreateView):
    """ 管理費支出データを登録する """
    model = Kanrihi_expense
    form_class = Kanrihi_expenseForm
    template_name = "kanrihi_out/kanrihi_expense_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    def get_success_url(self):
        return reverse('kanrihi_out:create_expense')

    def form_valid(self, form):
        """ 修繕会計への支出の場合、修繕会計の入金を同時に処理する """
        ki = form.cleaned_data['ki']
        account = form.cleaned_data['master']
        expense = form.cleaned_data['cost']
        if account == '修繕費繰入れ':
            Shuuzenhi_income.objects.create(ki=ki, master_id=7, income=expense)
            msg = f'第{ki}期の駐車場使用料繰入れを保存しました'
        else:
            msg = f'第{ki}期の管理会計支出を保存しました'
        messages.success(self.request, msg)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)


class UpdateExpenseView(PermissionRequiredMixin, generic.UpdateView):
    """ 管理費支出データを修正する """
    model = Kanrihi_expense
    form_class = Kanrihi_expenseForm
    template_name = "kanrihi_out/kanrihi_expense_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('kanrihi_out:update_list')

    def form_valid(self, form):
        """ 修繕会計の入金も処理する """
        ki = form.cleaned_data['ki']
        master = form.cleaned_data['master']
        expense = form.cleaned_data['expense']
        msg = ''
        if str(master) == '修繕費繰入れ':
            Shuuzenhi_income.objects.update_or_create(ki=ki+1, master_id=7, defaults={
                "income": expense,
            })
            msg = f'第{ki}期の修繕会計繰入れもアップデートしました'
        else:
            msg = f'第{ki}期の支出をアップデートしました'

        messages.info(self.request, msg)
        return super().form_valid(form)


class UpdateExpenselistView(PermissionRequiredMixin, generic.ListView):
    """ 管理費支出データ修正用listを表示する """
    model = Kanrihi_expense
    template_name = 'kanrihi_out/update_list.html'
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    ordering = ['-ki', 'master_id']
    paginate_by = 100


class CreateCategoryView(PermissionRequiredMixin, generic.CreateView):
    """ 管理費支出カテゴリーを登録する """
    model = Master_category
    form_class = Master_categoryForm
    template_name = "kanrihi_out/master_category_form.html"
    # 必要な権限
    permission_required = ("admin.add_logentry")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('kanrihi_out:create_category')

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
        context['masterlist'] = Master_category.objects.all().order_by('code')
        return context


class UpdateCategoryView(PermissionRequiredMixin, generic.UpdateView):
    """ 管理費支出カテゴリーを修正する """
    model = Master_category
    form_class = Master_categoryForm
    template_name = "kanrihi_out/master_category_form.html"
    # 必要な権限
    permission_required = ("admin.add_logentry")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('kanrihi_out:create_category')

    # マスターデータを表示させるため、get_context_dataをオーバーライド。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist'] = Master_category.objects.all()
        return context
