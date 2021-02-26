from django.urls import path
from asset_list import views

app_name = 'asset_list'
urlpatterns = [
    # データ表示
    path('assetlist/', views.AssetListView.as_view(), name='assetlist'),
    path('balance_sheet/', views.BalanceSheetView.as_view(), name='balance_sheet'),
    # データ登録
    path('create/', views.CreateAssetView.as_view(), name='create'),
    path('create_master',
         views.CreateMasterView.as_view(), name='create_master'),
    # 修正のための一覧表示
    path('update_list/',
         views.UpdateAssetlistView.as_view(), name='update_list'),
    # データ修正
    path('update/<int:pk>/', views.UpdateAssetView.as_view(), name='update'),
    path('update_master/<int:pk>/',
         views.UpdateMasterView.as_view(), name='update_master'),
    # CSVデータExport
    path('export/', views.asset_export, name='export'),

]
