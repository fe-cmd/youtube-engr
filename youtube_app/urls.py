from django.urls import path
from . import views

#33389
app_name = "youtube_app"

urlpatterns = [
	path('', views.ytb_down, name="ytb_down"),
    path('download/', views.ytb_download, name="ytb_download"),
    path('summarise/', views.start, name="start"),
    path('video_subtitles/', views.subtitle_ytb, name="subtitle_ytb"),
    path('downloads/', views.youtube, name='youtube'),
    path('search_results_videos/', views.search_ytb, name='search_ytb'),
    path('search_results_channels/', views.search_ytb1, name='search_ytb1'),
    path('search_results_playlists/', views.search_ytb2, name='search_ytb2'),
    path('show_filter/', views.show_filters, name='show_filters'),
    path('nlp_ai/', views.machine_models, name='machine_models'),   
    path('nlp_ai_res/', views.ai_ml_gen, name='ai_ml_gen'),
    path('match_nlp/', views.match_nlp, name="match-nlp"),    
	]