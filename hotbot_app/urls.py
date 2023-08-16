from django.urls import path
from .views import HotBotList, HotBotDetail

urlpatterns = [
    path('', HotBotList.as_view(), name='hotbot_list'),
    path('<int:pk>', HotBotDetail.as_view(), name='hotbot_detail'),
]