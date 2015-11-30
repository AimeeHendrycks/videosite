"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from main import views
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home),
    url(r'^base/$', views.base),

    url(r'^please_login/$', views.please_login),
    url(r'^channel_search/$', views.ChannelSearch.as_view()),
    url(r'^movie_search/$', views.MovieSearch.as_view()),
    url(r'^show_search/$', views.ShowSearch.as_view()),
    url(r'^episode_search/$', views.EpisodeSearch.as_view()),
    url(r'^person_search/$', views.PersonSearch.as_view()),
    url(r'^general_search/$', views.GeneralSearch.as_view()),
    url(r'^movie_detail/(?P<pk>\d+)/$', views.movie_detail),
    url(r'^channel_detail/(?P<pk>\d+)/$', views.ChannelDetail.as_view()),
    url(r'^show_detail/(?P<pk>\d+)/$', views.show_detail),
    url(r'^episode_detail/(?P<pk>\d+)/$', views.episode_detail),
    url(r'^channel_create/$', views.ChannelCreate.as_view()),
    url(r'^channel_update/(?P<pk>\d+)/$', views.ChannelUpdate.as_view()),
    url(r'^channel_delete/(?P<pk>\d+)/$', views.ChannelDelete.as_view()),
    url(r'^movie_create/$', views.MovieCreate.as_view()),
    url(r'^movie_update/(?P<pk>\d+)/$', views.MovieUpdate.as_view()),
    url(r'^show_delete/(?P<pk>\d+)/$', views.ShowDelete.as_view()),
    url(r'^show_create/$', views.ShowCreate.as_view()),
    url(r'^show_update/(?P<pk>\d+)/$', views.ShowUpdate.as_view()),
    url(r'^show_delete/(?P<pk>\d+)/$', views.ShowDelete.as_view()),
    url(r'^episode_delete/(?P<pk>\d+)/$', views.EpisodeDelete.as_view()),
    url(r'^episode_create/$', views.EpisodeCreate.as_view()),
    url(r'^episode_update/(?P<pk>\d+)/$', views.EpisodeUpdate.as_view()),
    url(r'^episode_delete/(?P<pk>\d+)/$', views.EpisodeDelete.as_view()),
    url(r'^add_show/(?P<pk>\d+)/$', views.add_show),
    url(r'^remove_show/(?P<pk>\d+)/$', views.remove_show),
    url(r'^add_movie/(?P<pk>\d+)/$', views.add_movie),
    url(r'^remove_movie/(?P<pk>\d+)/$', views.remove_movie),
    
    url(r'^respondmovie/(?P<pk1>\d+)/(?P<pk2>\d+)/(?P<num>\d+)/$', views.respondmovie),
    url(r'^remove_movie_response/(?P<response_pk>\d+)/(?P<movie_pk>\d+)/$', views.remove_movie_response),
    
    url(r'^commentmovie/(?P<pk>\d+)/$', views.commentmovie),
    url(r'^remove_movie_comment/(?P<comment_pk>\d+)/(?P<movie_pk>\d+)/$', views.remove_movie_comment),

    url(r'^replymovie/(?P<pk1>\d+)/(?P<pk2>\d+)/$', views.replymovie),
    url(r'^remove_movie_reply/(?P<reply_pk>\d+)/(?P<movie_pk>\d+)/$', views.remove_movie_reply),
    
    url(r'^respondshow/(?P<pk1>\d+)/(?P<pk2>\d+)/(?P<num>\d+)/$', views.respondshow),
    url(r'^remove_show_response/(?P<response_pk>\d+)/(?P<show_pk>\d+)/$', views.remove_show_response),

    url(r'^commentshow/(?P<pk>\d+)/$', views.commentshow),
    url(r'^remove_show_comment/(?P<comment_pk>\d+)/(?P<show_pk>\d+)/$', views.remove_show_comment),

    url(r'^replyshow/(?P<pk1>\d+)/(?P<pk2>\d+)/$', views.replyshow),
    url(r'^remove_show_reply/(?P<reply_pk>\d+)/(?P<show_pk>\d+)/$', views.remove_show_reply),

    url(r'^respondepisode/(?P<pk1>\d+)/(?P<pk2>\d+)/(?P<num>\d+)/$', views.respondepisode),
    url(r'^remove_episode_response/(?P<response_pk>\d+)/(?P<episode_pk>\d+)/$', views.remove_episode_response),

    url(r'^commentepisode/(?P<pk>\d+)/$', views.commentepisode),
    url(r'^remove_episode_comment/(?P<comment_pk>\d+)/(?P<episode_pk>\d+)/$', views.remove_episode_comment),

    url(r'^replyepisode/(?P<pk1>\d+)/(?P<pk2>\d+)/$', views.replyepisode),
    url(r'^remove_episode_reply/(?P<reply_pk>\d+)/(?P<episode_pk>\d+)/$', views.remove_episode_reply),

    url(r'^respondchannel/(?P<pk1>\d+)/(?P<pk2>\d+)/(?P<num>\d+)/$', views.respondchannel),
    url(r'^remove_channel_response/(?P<response_pk>\d+)/(?P<channel_pk>\d+)/$', views.remove_channel_response),

    url(r'^commentchannel/(?P<pk>\d+)/$', views.commentchannel),
    url(r'^remove_channel_comment/(?P<comment_pk>\d+)/(?P<channel_pk>\d+)/$', views.remove_channel_comment),

    url(r'^replychannel/(?P<pk1>\d+)/(?P<pk2>\d+)/$', views.replychannel),
    url(r'^remove_channel_reply/(?P<reply_pk>\d+)/(?P<channel_pk>\d+)/$', views.remove_channel_reply),

    url(r'^vote_movie/(?P<pk>\d+)/(?P<num>\d+)/$', views.vote_movie),
    url(r'^vote_show/(?P<pk>\d+)/(?P<num>\d+)/$', views.vote_show),
    url(r'^vote_episode/(?P<pk>\d+)/(?P<num>\d+)/$', views.vote_episode),
    url(r'^vote_channel/(?P<pk>\d+)/(?P<num>\d+)/$', views.vote_channel),

    url(r'^login/$', views.login_view),
    url(r'^signup/$', views.signup),
    url(r'^logout/$', views.logout_view),
    url(r'^profile/(?P<pk>\d+)/$', views.profile),
    url(r'^profile_update/(?P<pk>\d+)/$', views.ProfileUpdate.as_view()),

]
