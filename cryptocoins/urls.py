from django.conf.urls import url
from . import views



urlpatterns = [
    # url(r'^$', views.tips_list, name='tips_list'),

    url(r'^coins/update_all/$', views.Update_Coins, name='coins_update_all'),

]
