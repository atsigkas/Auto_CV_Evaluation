from django.urls import path
from . import views

urlpatterns = (
    path('', views.home, name="home"),
    path('api-endpoint/', views.upload_files , name='handle_array_data'),
    path('api-endpoint/Url', views.save_url , name='handle_array_data'),
    path('api-endpoint/RankingCandidates', views.ranking_candidates , name='handle_array_data'),
)
