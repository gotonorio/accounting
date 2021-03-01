from django.urls import path

from balance import views

app_name = 'balance'
urlpatterns = [
    # データ表示
    path('shuuzenhi/', views.ShuuzenhiBalanceView.as_view(), name='shuuzenhi'),
    path('check_shuuzenhi/', views.CheckShuuzenhiBalanceView.as_view(), name='check_shuuzenhi'),
    path('kanrihi/', views.KanrihiBalanceView.as_view(), name='kanrihi'),
    path('check_kanrihi/', views.CheckKanrihiBalanceView.as_view(), name='check_kanrihi'),
]
