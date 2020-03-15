from django.urls import path

from . import views

app_name = 'options'

urlpatterns = [
    path('', views.get_options_list),
    path('options/', views.get_options_list),
    path('options/index', views.get_options_list, name='get_options_list'),
    # path('license/search/', views.search, name='search_page'),
    # path('license/detail/<int:id>', views.get_detail_page),
    # path('license/404', views.page_not_found, name='page_not_found'),
    # path('license/500', views.page_server_error, name='page_server_error'),
]