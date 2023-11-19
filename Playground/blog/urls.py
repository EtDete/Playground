from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.personnage_list, name='personnage_list'),
    path('personnage/<str:id_personnage>/', views.post_detail, name='post_detail'),
    path('personnage/<str:id_personnage>/?<str:message>', views.post_detail, name='post_detail_mes'),
    path('add_character/', views.add_character, name='add_character'),
    path('add_place/', views.add_place, name='add_place'),

]