#!/usr/bin/env python
import sys, os, pprint, json
sys.path.append("..")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
from unidecode import unidecode

import django
django.setup()
from django.conf import settings
from main.models import Show

with open('show_json.txt') as data_file:
    data = json.load(data_file)

# print data
for show in data:
    try:
        new_show, created = Show.objects.get_or_create(show_id=show['show_id'])
        print new_show.show_id
        if show['title'] != None:
            new_show.title = str(unidecode(show['title']))
            print new_show.title
        new_show.imdb_id = show['imdb_id']
        new_show.first_aired = show['first_aired']
        new_show.rating = show['rating']
        new_show.artwork = show['artwork']
        if show['overview'] != None:
            new_show.overview = str(unidecode(show['overview']))
        new_show.runtime = show['runtime']
        new_show.upvote_count = show['upvote_count']
        new_show.downvote_count = show['downvote_count']
        new_show.save()
    except:
        print 'Nonetype'
    print '<<' + str(new_show.pk) +'>>'
