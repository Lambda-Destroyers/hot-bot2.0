from django.urls import path
from .views import CustomAdminLoginView, HotBotList, HotBotDetail, HotBotData, home

urlpatterns = [
    # path('', HotBotList.as_view(), name='hotbot_list'),
    path('', HotBotList.as_view(), name='home'),
    path('<int:pk>', HotBotDetail.as_view(), name='hotbot_detail'),
    path('admin/login/', CustomAdminLoginView.as_view(), name='admin_login'),
    path('crypto-page/', home, name='crypto_page'),
    path('hotbot-data/', HotBotData.as_view(), name='hotbot_data'),
]
