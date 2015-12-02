#!/usr/bin/env python
import sys, os, pprint, json
sys.path.append("..")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
from unidecode import unidecode

import django
django.setup()
from django.conf import settings
from main.models import Vote, Movie, Show, Channel, Episode, CustomUser

with open('vote_json.txt') as data_file:
    data = json.load(data_file)
inc = 0
# print data
for vote in data:
    inc += 1
    print inc

    new_vote, created = Vote.objects.get_or_create(vote_id=vote['vote_id'])
    new_vote.vote_type = str(unidecode(vote['vote_type']))
        new_vote.user = CustomUser.objects.get(email=vote['user'])
        print new_vote.display_name
    if vote['video_kind'] == 'show':
        new_vote.show = Show.objects.get(pk=vote['show'])
    if vote['video_kind'] == 'movie':
        new_vote.movie = Movie.objects.get(pk=vote['movie'])
    if vote['video_kind'] == 'episode':
        new_vote.episode = Episode.objects.get(pk=vote['episode'])
    if vote['video_kind'] == 'channel':
        new_vote.channel = Channel.objects.get(pk=vote['channel'])
   
    new_videosource.save()
    
    print '<<' + str(new_videosource.pk) +'>>'
