from django.urls import path

from parking_in import views

app_name = 'parking_in'
urlpatterns = [
    # データ表示
    path('incomelist/', views.IncomeListView.as_view(), name='incomelist'),
    # データ登録
    path('create', views.IncomeCreateView.as_view(), name='create'),
    # データ修正
    path('update_list/', views.UpdateListView.as_view(), name='update_list'),
    path('update/<int:pk>/', views.UpdateIncomeView.as_view(), name='update'),
]
