import logging
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Case, Sum, When
from django.views import generic

from kanrihi_in.models import Kanrihi_income
from kanrihi_out.views import KanrihiExpenseListView
from shuuzenhi_in.models import Shuuzenhi_income
from shuuzenhi_out.models import Rireki
from shuuzenhi_out.views import ShuuzenhiExpenseListView
# from parking_in.models import Parking_income


class KanrihiBalanceView(LoginRequiredMixin, generic.TemplateView):
    """ 管理会計収支リスト表示 """
    # template名の指定は必須
    template_name = "balance/balance_kanri.html"

    def get_context_data(self, **kwargs):
        """ 参考url http://thinkami.hatenablog.com/entry/2015/09/04/235841 """
        context = super().get_context_data(**kwargs)
        a = Kanrihi_income.objects.select_related().order_by('ki')
        income_qs = a.values('ki').annotate(
            zenki=Sum(Case(When(master__category__code=10, then='income'), default=0)),
            kanrihi_in=Sum(Case(
                When(master__category__code=20, then='income'),
                When(master__category__code=30, then='income'),
                default=0
             )),
            parking=Sum(
                Case(When(master__category__code=40, then='income'), default=0)),
            in_total=Sum(Case(
                When(master__category__code=10, then='income'),
                When(master__category__code=20, then='income'),
                When(master__category__code=30, then='income'),
                When(master__category__code=40, then='income'),
                default=0
             ))
        )
        expense_qs = KanrihiExpenseListView.kanrihi_expense(self)
        context['balancelist'] = self.make_balance_sheet(income_qs, expense_qs)
        return context

    def make_balance_sheet(self, incomelist, expenselist):
        """ income_qsとexpense_qsから必要な収支データを作成する。"""
        balance = []
        if len(incomelist) == len(expenselist):
            for i, income in enumerate(incomelist):
                income.update(expenselist[i])
                balance.append(income)
        return balance


class CheckKanrihiBalanceView(LoginRequiredMixin, generic.TemplateView):
    """ 管理会計収支リスト表示 """
    # template名の指定は必須
    template_name = "balance/check_kanrihi.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Kanrihi_income.objects.select_related().order_by('ki')
        income_qs = a.values('ki').annotate(
            zenki=Sum(Case(When(master__code=10, then='income'), default=0)),
            kanrihi_in=Sum(Case(
                When(master__code=20, then='income'), # 管理費収入
                When(master__category__code=30, then='income'), # その他収入
                default=0
            )),
            parking=Sum(
                Case(When(master__category__code=40, then='income'), default=0)),
            in_total=Sum(Case(
                When(master__category__code=10, then='income'),
                When(master__category__code=20, then='income'),
                When(master__category__code=30, then='income'),
                default=0
            ))
        )
        expense_qs = KanrihiExpenseListView.kanrihi_expense(self)
        context['balancelist'] = self.check_balance_sheet(income_qs, expense_qs)
        return context

    def check_balance_sheet(self, incomelist, expenselist):
        """ 計算結果から収支一覧を作成する。"""
        balance = []
        surplus = []
        if len(incomelist) == len(expenselist):
            # 収支計算用データ作成
            for i, income in enumerate(incomelist):
                # incomelistとexpenselistを一体化して処理する。
                income.update(expenselist[i])
                d = {}
                if i > 0:
                    zenki = surplus[i-1]
                else:
                    zenki = income['zenki']
                kanrihi_in = income['kanrihi_in']
                parking_in = income['parking']
                kanrihi_out = expenselist[i]['out_total']
                to_shuuzen = expenselist[i]['to_shuuzen']
                jyouyo = zenki+kanrihi_in+parking_in-kanrihi_out-to_shuuzen
                surplus.append(jyouyo)
                d['zenki'] = zenki
                d['surplus'] = jyouyo
                income.update(d)
                balance.append(income)
        return balance


class ShuuzenhiBalanceView(LoginRequiredMixin, generic.TemplateView):
    """ 修繕会計収支リスト表示 """
    # template名の指定は必須
    template_name = "balance/balance_shuuzen.html"

    def get_context_data(self, **kwargs):
        """ 参考url http://thinkami.hatenablog.com/entry/2015/09/04/235841 """
        context = super().get_context_data(**kwargs)
        a = Shuuzenhi_income.objects.select_related().order_by('ki')
        income_qs = a.values('ki').annotate(
            zenki=Sum(Case(When(master__code=10, then='income'), default=0)),
            shuuzenhi=Sum(Case(When(master__code=20, then='income'), default=0)),
            sonota=Sum(Case(
                When(master__code=25, then='income'),
                When(master__code=30, then='income'),
                When(master__code=35, then='income'),
                When(master__code=40, then='income'),
                When(master__code=60, then='income'),
                When(master__code=70, then='income'),
                When(master__code=80, then='income'),
                default=0
            )),
            parking=Sum(
                Case(When(master__code=50, then='income'), default=0)),
            in_total=Sum(
                Case(When(master__code__gte=10, then='income'), default=0)),
        )
        qs = Rireki.objects.select_related().order_by('year')
        expense_qs = ShuuzenhiExpenseListView.shuuzenhi_expense(self, qs)

        context['balancelist'] = self.make_balance_sheet(income_qs, expense_qs)
        context["start_year"] = settings.START_YEAR
        return context

    def make_balance_sheet(self, incomelist, expenselist):
        """ income_qsとexpense_qsから必要な収支データを作成する。"""
        balance = []
        num1 = len(incomelist)
        num2 = len(expenselist)

        if num1 == num2:
            for i, income in enumerate(incomelist):
                income.update(expenselist[i])
                balance.append(income)
        return balance


class CheckShuuzenhiBalanceView(LoginRequiredMixin, generic.TemplateView):
    """ 修繕会計収支リスト表示 """
    # template名の指定は必須
    template_name = "balance/check_shuuzen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Shuuzenhi_income.objects.select_related().order_by('ki')
        income_qs = a.values('ki').annotate(
            zenki=Sum(Case(When(master__code=10, then='income'), default=0)),
            shuuzenhi=Sum(Case(When(master__code=20, then='income'), default=0)),
            sonota=Sum(Case(
                When(master__code=25, then='income'),
                When(master__code=30, then='income'),
                When(master__code=35, then='income'),
                When(master__code=40, then='income'),
                When(master__code=60, then='income'),
                When(master__code=70, then='income'),
                When(master__code=80, then='income'),
                default=0
            )),
            parking=Sum(
                Case(When(master__code=50, then='income'), default=0)),
            in_total=Sum(
                Case(When(master__code__gte=10, then='income'), default=0)),
        )
        qs = Rireki.objects.select_related().order_by('year')
        expense_qs = ShuuzenhiExpenseListView.shuuzenhi_expense(self, qs)

        context['balancelist'], debug = self.check_balance_sheet(income_qs, expense_qs)
        context["start_year"] = settings.START_YEAR
        return context

    def check_balance_sheet(self, incomelist, expenselist):
        """ 計算結果から収支一覧を作成する。"""
        balance = []
        surplus = []
        if len(incomelist) == len(expenselist):
            # 収支計算用データ作成
            for i, income in enumerate(incomelist):
                # incomelistとexpenselistを一体化して処理する。
                income.update(expenselist[i])
                d = {}
                if i > 0:
                    zenki = surplus[i-1]
                else:
                    zenki = income['zenki']
                shuuzenhi = income['shuuzenhi']
                parking = income['parking']
                sonota = income['sonota']
                total = zenki + shuuzenhi + parking + sonota
                shuuzen_out = expenselist[i]['shuuzen']
                jyouyo = zenki + shuuzenhi + parking + sonota - shuuzen_out
                logging.debug(sonota)
                surplus.append(jyouyo)
                d['zenki'] = zenki
                d['surplus'] = jyouyo
                d['in_total'] = total
                income.update(d)
                balance.append(income)
        return balance, surplus
