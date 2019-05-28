from django.urls import path

from PumpManager import views


urlpatterns = [
    path('', views.index, name='index'),
    #path('profile/<nickname>/', views.uniqueProfile, name='uniqueProfile'),

    path('statistic/', views.statistic, name='statistic'),
    path('random/', views.random, name='random'),
    path('lists/', views.lists, name='lists'),
    path('songs/', views.songs, name='songs'),
    path('songs/<song_id>', views.songID, name='songID'),

    path('mixes/', views.mixes, name='mixes'),
    path('mixes/<mix_id>', views.mixID, name='mixID'),

    path('register/', views.RegisterFormView.as_view(), name='register'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/settings', views.profile_settings, name = 'profile_settings'),

    path('locations/', views.locations, name = 'locations') ,
]
