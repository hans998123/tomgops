from django.urls import path

from tomopsapp import views

urlpatterns = [
   path('',views.index),
   path('index/',views.work),
   path('register/',views.register),
   path('login/',views.login),
   path('logout/',views.logout),
   path('reset_password/',views.reset_password),
   path('update_password/',views.update_password),
   path('index/get_user_info/', views.get_user_info),
   path('index/get_user_dovecot_info/', views.get_user_dovecot_info),
   path('index/get_user_quota_info/', views.get_user_quota_info),
   path('index/recalc_user_quota_info/', views.recalc_user_quota_info),
   path('index/change_user_quota_info/', views.change_user_quota_info),
   path('index/get_domain_blacklist_info/', views.get_domain_blacklist_info),
   path('index/get_ip_blacklist_info/',views.get_ip_blacklist_info),
   path('index/get_mailuser_send_number_info/',views.get_mailuser_send_number_info),
   path('index/add_barracuda_whitelist_info/',views.add_barracuda_whitelist_info),
]