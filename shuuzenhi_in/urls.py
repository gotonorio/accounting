from django.urls import path

from shuuzenhi_in import views

app_name = 'shuuzenhi_in'
urlpatterns = [
    # データ表示
    path('incomelist/', views.IncomeListView.as_view(), name='incomelist'),
    path('uchiwakelist/',
         views.UchiwakeListView.as_view(), name='uchiwakelist'),
    # データ登録
    path('create', views.CreateIncomeView.as_view(), name='create'),
    path('create_master',
         views.CreateMasterView.as_view(), name='create_master'),
    # データ修正
    path('update_list/', views.DatalistView.as_view(), name='update_list'),
    path('update_master/<int:pk>/',
         views.UpdateMasterView.as_view(), name='update_master'),
    path('update/<int:pk>/', views.UpdateIncomeView.as_view(), name='update'),
#    # CSVデータExport
#    path('export/', views.shuuzenhi_in_export, name='export'),
]
