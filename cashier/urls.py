from django.urls import path
from cashier import views

app_name = 'cashier'
urlpatterns = [
    # データ表示
    path('list/', views.CashierListView.as_view(), name='list'),
    # データ登録
    path('create/', views.CashierCreateView.as_view(), name='create'),
    path('update/<int:pk>', views.CashierUpdateView.as_view(), name='update'),
]
