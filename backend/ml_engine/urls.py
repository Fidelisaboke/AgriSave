from django.urls import path
from . import views

urlpatterns = [
    path('predict-disease/', views.predict_disease, name='predict_disease'),
    path('recommend-crops/', views.recommend_crops, name='recommend_crops'),
    path('climate-forecast/', views.climate_forecast, name='climate_forecast'),
    path('status/', views.ml_status, name='ml_status'),
]