from django.urls import path

from parking_out import views

app_name = 'parking_out'
urlpatterns = [
    # データ表示
    path('expendlist/', views.ExpenditureListView.as_view(), name='expendlist'),
    # データ登録
    path('create', views.ExpenditureCreateView.as_view(), name='create'),
    # データ修正
    path('update_list/', views.UpdateListView.as_view(), name='update_list'),
    path('update/<int:pk>/', views.UpdateExpenditureView.as_view(), name='update'),
]
