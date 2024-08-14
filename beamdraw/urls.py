from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('beam-data/', views.beam_design_view, name='beam_data'),
]