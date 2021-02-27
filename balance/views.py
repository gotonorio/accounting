# import logging
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Case, Sum, When
from django.views import generic

from kanrihi_in.models import Kanrihi_income
from kanrihi_out.views import KanrihiExpenseListView
from shuuzenhi_in.models import Shuuzenhi_income
from shuuzenhi_out.models import Rireki
from shuuzenhi_out.views import ShuuzenhiExpenseListView
from parking_in.models import Parking_income


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
        num1 = len(incomelist)
        num2 = len(expenselist)
        if num1 == num2:
            for i, income in enumerate(incomelist):
                income.update(expenselist[i])
                balance.append(income)
        return balance


class NewKanrihiBalanceView(LoginRequiredMixin, generic.TemplateView):
    """ 管理会計収支リスト表示 """
    # template名の指定は必須
    template_name = "balance/balance_kanri2.html"

    def get_context_data(self, **kwargs):
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
                # When(master__category__code=40, then='income'),
                default=0
             ))
        )
        expense_qs = KanrihiExpenseListView.kanrihi_expense(self)
        context['balancelist'] = self.make_balance_sheet(income_qs, expense_qs)
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


class ParkingBalanceView(LoginRequiredMixin, generic.TemplateView):
    """ 駐車場会計収支リスト表示 """
    # template名の指定は必須
    template_name = "balance/balance_parking.html"

    def get_context_data(self, **kwargs):
        """ 参考url http://thinkami.hatenablog.com/entry/2015/09/04/235841 """
        context = super().get_context_data(**kwargs)
        a = Parking_income.objects.select_related().order_by('ki')
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