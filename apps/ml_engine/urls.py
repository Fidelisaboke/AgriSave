from django.urls import path
from . import views

urlpatterns = [
    path('predict-disease/', views.predict_disease, name='predict_disease'),
    path('recommend-crop/', views.recommend_crop, name='recommend_crop'),
    path('climate-forecast/', views.climate_forecast, name='climate_forecast'),
    path('status/', views.ml_status, name='ml_status'),
]