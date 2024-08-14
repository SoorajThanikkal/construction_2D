from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('beam-data/', views.beam_data, name='beam_data'),
]