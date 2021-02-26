from django.urls import path
from kanrihi_in import views

app_name = 'kanrihi_in'
urlpatterns = [
    # データ表示
    path('incomelist/',
         views.IncomeListView.as_view(), name='incomelist'),
    path('uchiwakelist/',
         views.UchiwakeListView.as_view(), name='uchiwakelist'),
    # データ登録
    path('create_income',
         views.CreateIncomeView.as_view(), name='create_income'),
    path('create_master',
         views.CreateMasterView.as_view(), name='create_master'),
    # 修正のための一覧表
    path('update_list/',
         views.UpdateIncomelistView.as_view(), name='update_list'),
    path('update/<int:pk>/',
         views.UpdateIncomeView.as_view(), name='update'),
    path('update_master/<int:pk>/',
         views.UpdateMasterView.as_view(), name='update_master'),
    path('create_category',
         views.CreateCategoryView.as_view(), name='create_category'),
    path('update_category/<int:pk>/',
         views.UpdateCategoryView.as_view(), name='update_category'),
#    # CSVデータExport
#    path('export/', views.kanrihi_in_export, name='export'),
]
