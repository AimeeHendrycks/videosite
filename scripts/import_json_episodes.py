#!/usr/bin/env python
import sys, os, pprint, json
sys.path.append("..")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
from unidecode import unidecode

import django
django.setup()
from django.conf import settings
from main.models import Episode

with open('episode_json.txt') as data_file:
    data = json.load(data_file)
from unidecode import unidecode

# print data
for episode in data:
    try:
        new_episode, created = Episode.objects.get_or_create(episode_id=episode['episode_id'])
        print new_episode.episode_id
        if episode['title'] != None:
            new_episode.title = str(unidecode(episode['title']))
            print new_episode.title
        new_episode.imdb_id = episode['imdb_id']
        new_episode.first_aired = episode['first_aired']
        new_episode.season_number = episode['season_number']
        new_episode.episode_number = episode['episode_number']
        new_episode.show = episode['show']
        new_episode.artwork = episode['artwork']
        if episode['overview'] != None:
            new_episode.overview = str(unidecode(episode['overview']))
        new_episode.upvote_count = episode['upvote_count']
        new_episode.downvote_count = episode['downvote_count']
        new_episode.save()
    except:
        print 'Nonetype'
    print '<<' + str(new_episode.pk) +'>>'
