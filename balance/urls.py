from django.urls import path

from balance import views

app_name = 'balance'
urlpatterns = [
    # データ表示
    path('shuuzenhi/', views.ShuuzenhiBalanceView.as_view(), name='shuuzenhi'),
    path('kanrihi/', views.KanrihiBalanceView.as_view(), name='kanrihi'),
    path('kanrihi2/', views.NewKanrihiBalanceView.as_view(), name='kanrihi2'),
]
