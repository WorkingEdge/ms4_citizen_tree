from django.urls import path

urlpatterns = [
    path('', views.calc, name='calc'),
]