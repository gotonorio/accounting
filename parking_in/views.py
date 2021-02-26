from django.contrib import messages  # メッセージフレームワーク
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import reverse
from django.views import generic

from parking_in.forms import Parking_incomeForm
from parking_in.models import Parking_income


class IncomeListView(LoginRequiredMixin, generic.TemplateView):
    """ 駐車場収入リスト一覧 """
    model = Parking_income
    template_name = "parking_in/income_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incomelist'] = Parking_income.objects.all().order_by('ki')
        return context


class IncomeCreateView(PermissionRequiredMixin, generic.CreateView):
    """ 駐車場収入データの登録
        自動的にform変数を作成してテンプレートに渡す。
        http://k-mawa.hateblo.jp/entry/2017/10/20/181711
        管理者権限を持つユーザーのみが使用可能とする。（パーミッション機能）
        https://torina.top/detail/295/
    """
    model = Parking_income
    form_class = Parking_incomeForm
    template_name = "parking_in/parking_income_form.html"
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl。プロパティ(seccess_url)を使うか、関数をオーバーライド。
    def get_success_url(self):
        return reverse('parking_in:create')

    # データvalidationが成功したら、直ぐにコミットせず、userを追加してから保存する例。
    # 以下はuserを入力させずに、既定値を登録する例として残す。
    def form_valid(self, form):
        # self.object = form.save(commit=False)
        # self.object.user = self.request.user
        # self.object.save()
        messages.success(self.request, "保存しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした。")
        return super().form_invalid(form)


class UpdateListView(PermissionRequiredMixin, generic.ListView):
    """ 駐車場収入データ修正用listを表示
        https://docs.djangoproject.com/ja/2.0/topics/pagination/
        http://thinkami.hatenablog.com/entry/2016/02/04/231901
    """
    model = Parking_income
    template_name = 'parking_in/update_list.html'
    # 必要な権限
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    ordering = ['-ki']
    paginate_by = 50


class UpdateIncomeView(PermissionRequiredMixin, generic.UpdateView):
    """ 駐車場収入データを修正する
    """
    model = Parking_income
    form_class = Parking_incomeForm
    template_name = "parking_in/parking_income_form.html"
    # 必要な権限（データ登録できる権限は共通）
    permission_required = ("asset_list.add_assetlist")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True

    # 保存が成功した場合に遷移するurl
    def get_success_url(self):
        return reverse('parking_in:update_list')
