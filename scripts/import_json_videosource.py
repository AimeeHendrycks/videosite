#!/usr/bin/env python
import sys, os, pprint, json
sys.path.append("..")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
from unidecode import unidecode

import django
django.setup()
from django.conf import settings
from main.models import VideoSource, Show, Movie

with open('videosource_json.txt') as data_file:
    data = json.load(data_file)
inc = 0
# print data
for videosource in data:
    inc += 1
    print inc

    new_videosource, created = VideoSource.objects.get_or_create(source_link=videosource['source_link'])
    print new_videosource.source_link
    if videosource['display_name'] != None:
        new_videosource.display_name = str(unidecode(videosource['display_name']))
        print new_videosource.display_name
    if videosource['video_type'] == 'show':
        new_videosource.show = Show.objects.get(pk=videosource['show'])
    if videosource['video_type'] == 'movie':
        new_videosource.movie = Movie.objects.get(pk=videosource['movie'])
   
    new_videosource.save()
    
    print '<<' + str(new_videosource.pk) +'>>'
