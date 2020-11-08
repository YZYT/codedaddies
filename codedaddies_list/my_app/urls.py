from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.home, name='home_page'),
    path('new-search', views.new_search, name='new_search'),
]
