from django.urls import path
#now import the views.py file into this code
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
  path('',views.home, name='index'),
  path('about/', views.about, name='about'),
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('save_user/', views.save_user, name='save_user'),
  path('login_user/', views.login_user, name='login_user'),
  path('services/', views.services, name='services'),
  path('add_services/', views.add_services, name='add_services'),
  path('service_provider/', views.service_provider, name='service_provider'),
  path('save_service_provider/', views.save_service_provider, name='save_service_provider'),
  path('login_service/', views.login_service, name='login_service'),
  path('login_service_provider/', views.login_service_provider, name='login_service_provider'),
  path('add_shop/', views.add_shop, name='add_shop'),
  path('save_shop/', views.save_shop, name='save_shop'),
  path('view_shops/', views.view_shops, name='view_shops'),
  path('view_shops_provider/', views.view_shops_provider, name='view_shops_provider'),
  path('get-default-recommendations/', views.get_default_recommendations, name='get_default_recommendations'),
  path('get-filtered-recommendations/', views.get_filtered_recommendations, name='get_filtered_recommendations'),
  path('fetch_providers_list/', views.fetch_providers_list, name='fetch_providers_list'),
  path('view_individual_shop/<str:shopid>/<str:service>/<str:area>/<str:city>/', views.view_individual_shop, name='view_individual_shop'),
  path('delete_shop', views.delete_shop, name='delete_shop'),
  path('delete_service', views.delete_service, name='delete_service'),
  path('users_list', views.users_list, name='users_list'),
  path('service_provider_list', views.service_provider_list, name='service_provider_list'),
  path('admin_page', views.admin_page, name='admin_page'),
  path('show_directions', views.show_directions, name='show_directions'),
  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)