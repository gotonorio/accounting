# import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Q, F
from django.db.models.aggregates import Case, Max, Sum, When
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, reverse
from django.views import generic

# from file_storage.models import File
from shuuzenhi_out.forms import (ConstractorForm, Master_koujitypeForm,
                                 SelectClassForm, Shuuzenhi_expenseForm)
from shuuzenhi_out.models import Constractor, Master_koujitype, Shuuzenhi_expense


class RirekiListView(LoginRequiredMixin, generic.TemplateView):
    """ 個別工事リスト
        1. contextを返さなくてもobject_list(単数ならobject)でテンプレートから参照できる．
        2. filter()を使わなければquerysetだけでget_context_data()が必要ない．
        3. queryset = Swap.objects.all().order_by('-hiduke')
        4. TemplateViewではtemplate_nameは必要。
        http://tnakamura.hatenablog.com/entry/20111110/django_class_based_generic_view
    """
    model = Shuuzenhi_expense
    # form_classはどのような時に必要か？
    form_class = SelectClassForm
    # TemplateViewの場合はtemplate_nameは必須．
    template_name = "shuuzenhi_out/rireki_list.html"

    # テンプレートで扱うときのクエリセットの名前を指定
    # 今回はcontextで抽出オブジェクトを返しているから必要ない。
    # context_object_name = "rirekilist"
    # get_context_data の引数の kwargs には、urls.py で指定した名前つきの
    # 正規表現のプレースホルダにマッチした内容が入ってくるが、
    # この内容は self.kwargs にも入っていてアクセスできる。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.request.user
        # formのselect要素の値を得る
        kouji_type = self.request.GET.get('kouji_type', '0')
        ac_type = self.request.GET.get('account_type', 'ALL')
        yyyy = Shuuzenhi_expense.objects.aggregate(year=Max('year'))['year']
        # 初期値として当年を設定。
        year = self.request.GET.get('year', yyyy)
        # ''が返された時の処理
        if kouji_type == '':
            kouji_type = '0'
        if year == '':
            year = '0'

        # Qオブジェクト作成
        koujitype_q = Q()
        actype_q = Q()
        year_q = Q()
        if kouji_type != '0':
            koujitype_q = Q(koujitype=kouji_type)
        if ac_type != 'ALL':
            actype_q = Q(account_type=ac_type)
        if year != '0':
            year_q = Q(year=year)
        sql = Shuuzenhi_expense.objects.filter(koujitype_q & actype_q & year_q).order_by('-year')

        # formのselectに初期値を設定する．http://i2bskn.hateblo.jp/entry/20120826/1345936779
        form = SelectClassForm(
            initial={'kouji_type': kouji_type, 'account_type': ac_type, 'year': year})

        # コストの合計を計算する
        total = Shuuzenhi_expense.calc_total(self, sql)
        context["total"] = total
        context["user_name"] = user_name
        context["form"] = form
        context["rirekilist"] = sql
        context["start_year"] = -settings.START_YEAR
        return context


class ExpenseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Shuuzenhi_expense
    template_name = "shuuzenhi_out/rireki_detail.html"


class ShuuzenhiExpenseListView(LoginRequiredMixin, generic.TemplateView):
    """ 年度別支出データ一覧を表示する """
    model = Shuuzenhi_expense
    # TemplateViewの場合はtemplate_nameは必須．
    template_name = "shuuzenhi_out/expense_list.html"

    def shuuzenhi_expense(self, qs):
        """ 別アプリ（shuuzenhi_in）で呼び出すため、独立した関数とする。
        http://thinkami.hatenablog.com/entry/2015/09/04/235841
        行の集約：values().annotate()の順番で記述する．
        values()：集約キー
        annotate()：下記を参照
        支出合計には修繕費会計への支出分は含めない。2018/03/25
        """
        expenselist = qs.values('year').annotate(
            shuuzen=Sum(Case(When(account_type='修繕費会計', then='cost'), default=0)),
            kanri=Sum(Case(When(account_type='管理費会計', then='cost'), default=0)),
            hoken=Sum(Case(When(account_type='保険対応', then='cost'), default=0)),
            total=F('kanri')+F('shuuzen')
        )
        return expenselist

    def get_context_data(self, **kwargs):
        # はじめに継承元のメソッドを呼び出す．
        context = super().get_context_data(**kwargs)
        # 大規模修繕費を表示すると、全体のバランスが崩れるためmypageのメニューで分ける。
        sw = self.kwargs.get('sw', 0)
        if sw == 1:
            a = Shuuzenhi_expense.objects.select_related().order_by('year')
        else:
            # a = Shuuzenhi_expense.objects.filter(koujitype__lt=20).select_related().order_by('year')
            a = Shuuzenhi_expense.objects.exclude(koujitype=20).select_related().order_by('year')

        context['expenselist'] = self.shuuzenhi_expense(a)
        # aggregateは辞書型を返すようだ。
        # 大規模修繕を外すためにid(20)を決め打ちしている。あまり良く無い！
        if sw == 1:
            context['shuuzen_total'] = Shuuzenhi_expense.objects.filter(
                account_type='修繕費会計').aggregate(Sum('cost'))['cost__sum']
            context["title"] = "工事支出履歴（大規模修繕含む)"
        else:
            context['shuuzen_total'] = Shuuzenhi_expense.objects.filter(
                account_type='修繕費会計').filter(
                koujitype__lt=20).aggregate(Sum('cost'))['cost__sum']
            context["title"] = "工事支出履歴（大規模修繕含まず)"

        context['kanri_total'] = Shuuzenhi_expense.objects.filter(
            account_type='管理費会計').aggregate(Sum('cost'))['cost__sum']
        context['hoken_total'] = Shuuzenhi_expense.objects.filter(
            account_type='保険対応').aggregate(Sum('cost'))['cost__sum']
        context['all_total'] = context['shuuzen_total']+context['kanri_total']+context['hoken_total']
        context["start_year"] = -settings.START_YEAR
        return context


class KoujiShubetuListView(LoginRequiredMixin, generic.TemplateView):
    """ 修繕工事の工事種別毎の支出一覧 """
    model = Shuuzenhi_expense
    template_name = "shuuzenhi_out/shubetu_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 大規模修繕は除く。
        a = Shuuzenhi_expense.objects.all().exclude(
            koujitype__koujitype='大規模修繕').order_by('koujitype__sequense')
        context['shubetulist'] = a.values(
            'koujitype__koujitype').annotate(total=Sum('cost'))
        return context


class CreateExpenseView(PermissionRequiredMixin, generic.CreateView):
    """ 修繕費支出データを登録する """
    model = Shuuzenhi_expense
    form_class = Shuuzenhi_expenseForm
    template_name = "shuuzenhi_out/rireki_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('shuuzenhi_out:create')

    def form_valid(self, form):
        messages.success(self.request, "保存しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)


class CreateKoujiTypeView(PermissionRequiredMixin, generic.CreateView):
    """ 修繕費の工事種別マスターを登録/修正する。
        マスターデータは、数が多くはないので表示しながら入力formを表示させる。
        データが存在すれば表示し、修正か新規登録させる。
        listでページングする場合は https://torina.top/detail/337/#i3 を参照。
    """
    model = Master_koujitype
    form_class = Master_koujitypeForm
    template_name = "shuuzenhi_out/master_koujitype_form.html"
    # 必要な権限
    permission_required = ("admin.add_logentry")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('shuuzenhi_out:create_koujitype')

    def form_valid(self, form):
        """ 上手く保存メッセージを表示できない？ """
        messages.success(self.request, "保存しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist'] = Master_koujitype.objects.all().order_by('sequense')
        return context


class UpdateKoujitypeView(PermissionRequiredMixin, generic.UpdateView):
    """ 修繕費支出項目マスターを修正する """
    model = Master_koujitype
    form_class = Master_koujitypeForm
    template_name = "shuuzenhi_out/master_koujitype_form.html"
    # 必要な権限
    permission_required = ("admin.add_logentry")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('shuuzenhi_out:create_koujitype')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist'] = Master_koujitype.objects.all().order_by('sequense')
        return context


class CreateConstractorView(PermissionRequiredMixin, generic.CreateView):
    """ 施工業者マスターを登録/修正する。
        データが存在すれば表示し、修正か新規登録させる。
        listでページングする場合は https://torina.top/detail/337/#i3 を参照。
    """
    model = Constractor
    form_class = ConstractorForm
    paginate_by = 4
    template_name = "shuuzenhi_out/constractor_form.html"
    # 必要な権限
    permission_required = ("admin.add_logentry")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('shuuzenhi_out:create_constractor')

    def form_valid(self, form):
        messages.success(self.request, "保存しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist'] = Constractor.objects.all().order_by('sequense')
        return context


class UpdateConstractorView(PermissionRequiredMixin, generic.UpdateView):
    """ 施工業者マスターを修正する """
    model = Constractor
    form_class = ConstractorForm
    template_name = "shuuzenhi_out/constractor_form.html"
    # 必要な権限
    permission_required = ("admin.add_logentry")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('shuuzenhi_out:create_constractor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist'] = Constractor.objects.all().order_by('sequense')
        return context


class RirekiUpdateListView(PermissionRequiredMixin, generic.ListView):
    """ 修繕費支出データ修正用listを表示
        https://docs.djangoproject.com/ja/2.0/topics/pagination/
        http://thinkami.hatenablog.com/entry/2016/02/04/231901
    """
    model = Shuuzenhi_expense
    template_name = 'shuuzenhi_out/rireki_update_list.html'
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    ordering = ['-year', 'koujitype']
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start_year'] = -settings.START_YEAR
        return context


class UpdateRirekiView(PermissionRequiredMixin, generic.UpdateView):
    """ 修繕費支出データを修正する。
        修正する工事が選択されると呼ばれる。
    """
    model = Shuuzenhi_expense
    form_class = Shuuzenhi_expenseForm
    template_name = "shuuzenhi_out/rireki_form.html"
    # 必要な権限（データ登録できる権限は共通）
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('shuuzenhi_out:update_list')


# class QuotationListView(FormMixin, generic.ListView):
#     """ 見積書一覧用View
#     ListViewでFormを使用する場合、FormMixinが必要。
#     https://stackoverflow.com/questions/6406553/django-class-based-view-listview-with-form
#     """
#     model = File
#     form_class = QuotationForm
#     template_name = "shuuzenhi_out/quotation_list.html"
#     paginate_by = 15
#
#     def get_queryset(self):
#         """ Formで指定されたcategoryを取り込んでquerysetを上書きする """
#         category = self.request.GET.get('category')
#         if category is None:
#             queryset = File.objects.all().order_by('-created_at')
#         else:
#             queryset = File.objects.filter(
#                 category=category).order_by('-created_at')
#
#         return queryset


def view_quotation(request, pk):
    """ 見積書ファイルを表示 """
    pdf_file = get_object_or_404(File, pk=pk)
    response = HttpResponse(pdf_file.src, content_type='application/pdf')
    return response
