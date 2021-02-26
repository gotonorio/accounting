from django.urls import path

from kanrihi_out import views

app_name = 'kanrihi_out'
urlpatterns = [
    # データ表示
    path('expenselist/',
         views.KanrihiExpenseListView.as_view(), name='expenselist'),
    path('breakdownlist/',
         views.BreakdownListView.as_view(), name='breakdownlist'),
    # データの登録／修正
    path('create_expense',
         views.CreateExpenseView.as_view(), name='create_expense'),
    path('update_list/',
         views.UpdateExpenselistView.as_view(), name='update_list'),
    path('update/<int:pk>/',
         views.UpdateExpenseView.as_view(), name='update'),
    path('create_master',
         views.CreateMasterView.as_view(), name='create_master'),
    path('update_master/<int:pk>/',
         views.UpdateMasterView.as_view(), name='update_master'),
    path('create_category',
         views.CreateCategoryView.as_view(), name='create_category'),
    path('update_category/<int:pk>/',
         views.UpdateCategoryView.as_view(), name='update_category'),
#    # CSVデータExport
#    path('export/', views.kanrihi_out_export, name='export'),
]
