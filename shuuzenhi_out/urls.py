from django.urls import path

from shuuzenhi_out import views

app_name = 'shuuzenhi_out'
urlpatterns = [
    # データ表示
    path('rirekilist/', views.RirekiListView.as_view(), name='rirekilist'),
    path('shubetulist/',
         views.KoujiShubetuListView.as_view(), name='shubetulist'),
    path('expenselist/',
         views.ShuuzenhiExpenseListView.as_view(), name='expenselist'),
    path('expenselist/<int:sw>',
         views.ShuuzenhiExpenseListView.as_view(), name='expenselist'),
    path('detail/<int:pk>',
         views.ExpenseDetailView.as_view(), name='detail'),
    #path('quotation/',
    #     views.QuotationListView.as_view(), name='quotation'),
    path('view_quotation/<int:pk>', views.view_quotation, name='view_quotation'),
    # データ登録
    path('create',
         views.CreateExpenseView.as_view(), name='create'),
    path('create_koujitype', views.CreateKoujiTypeView.as_view(),
         name='create_koujitype'),
    path('create_constractor', views.CreateConstractorView.as_view(),
         name='create_constractor'),
    # データ修正
    path('update_list/', views.RirekiUpdateListView.as_view(), name='update_list'),
    path('update/<int:pk>/', views.UpdateRirekiView.as_view(), name='update'),
    #path('update_accounttype/<int:pk>/',
    #     views.UpdateAccountingTypeView.as_view(), name='update_accounttype'),
    path('update_koujitype/<int:pk>/',
         views.UpdateKoujitypeView.as_view(), name='update_koujitype'),
    path('update_constractor/<int:pk>/',
         views.UpdateConstractorView.as_view(), name='update_constractor'),
    # # CSVデータExport
    # path('export/', views.shuuzenhi_out_export, name='export'),
    #     # BigCategoruに属するファイルを一覧表示
    # path('bigcategory/<int:pk>/',
    #      views.BigCategoryView.as_view(), name='bigcategory'),
]
