import calendar
import datetime

from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import AccountSubjectListForm, ExpenditureForm
from .models import Account_subject


def set_year_month(year, month):
    """ 年月がFalseなら当月を返す """
    now = timezone.localtime(timezone.now())
    if year is None:
        year = now.year
    else:
        year = int(year)
    if month is None:
        month = now.month
    else:
        month = int(month)
    return year, month


class CashierListView(LoginRequiredMixin, generic.TemplateView):
    """ 管理費収入リスト表示 """
    model = Account_subject
    template_name = "cashier/cashier_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        year, month = set_year_month(year, month)
        if month < 1:
            first_month = 1
            last_month = 12
        else:
            first_month = month
            last_month = first_month
        # 任意の年月の日数をcalendarで求める。
        _, dd = calendar.monthrange(year, last_month)
        # 任意の年月の初日のdatetimeオブジェクト
        first_day = datetime.date(year, first_month, 1)
        # 任意の年月の最終日のdatetimeオブジェクト
        last_day = datetime.date(year, last_month, dd)
        qs = Account_subject.objects.all()
        qs = qs.filter(spending_date__gte=first_day, spending_date__lte=last_day)
        qs = qs.order_by('-spending_date')
        form = AccountSubjectListForm(initial={
            'year': year,
            'month': month,
        })
        total = 0
        for data in qs:
            total += data.expense
        context['objects_list'] = qs
        context['total'] = total
        context['form'] = form
        return context


class CashierCreateView(PermissionRequiredMixin, generic.CreateView):
    """ 小口会計データ入力 """
    model = Account_subject
    form_class = ExpenditureForm
    template_name = "cashier/expense_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy('cashier:create')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CashierUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Account_subject
    form_class = ExpenditureForm
    template_name = "cashier/expense_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy('cashier:create')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)
