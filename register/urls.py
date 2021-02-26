from django.urls import path
from register.views import (MypageView, OperateDataView,
                            OperateRepairDataView, Login, Logout)


"""
https://torina.top/detail/222/
"""
app_name = 'register'
urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('mypage', MypageView.as_view(), name='mypage'),
    path('operate_data/', OperateDataView.as_view(), name='operate_data'),
    path('operate_repair_data/', OperateRepairDataView.as_view(),
         name='operate_repair_data'),
]
