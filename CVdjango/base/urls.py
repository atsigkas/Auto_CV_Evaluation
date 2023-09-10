from django.urls import path
from . import views

urlpatterns = (
    path('', views.home, name="home"),
    path('api-endpoint/', views.upload_files , name='handle_array_data'),

)
