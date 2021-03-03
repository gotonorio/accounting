from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from .forms import LoginForm


class MypageView(LoginRequiredMixin, TemplateView):
    template_name = "register/mypage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['user_id'] = self.request.user.id
        return context


class OperateDataView(LoginRequiredMixin, TemplateView):
    template_name = "register/operate_data.html"


class OperateRepairDataView(LoginRequiredMixin, TemplateView):
    template_name = "register/operate_repair_data.html"


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'register/logout.html'


class MasterDataView(LoginRequiredMixin, TemplateView):
    template_name = "register/master_data.html"
