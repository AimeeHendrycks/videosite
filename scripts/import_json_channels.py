#!/usr/bin/env python
import sys, os, pprint, json
sys.path.append("..")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
from unidecode import unidecode

import django
django.setup()
from django.conf import settings
from main.models import Channel, Show

with open('channel_json.txt') as data_file:
    data = json.load(data_file)

# print data
for channel in data:
    new_channel, created = Channel.objects.get_or_create(channel_id=channel['channel_id'])
    print new_channel.channel_id
    if channel['title'] != None:
        new_channel.title = str(unidecode(channel['title']))
        print new_channel.title
    
    new_channel.artwork = channel['artwork']
    for s in channel['shows']:
        print s
        # new_channel.show.add(Show.objects.get(show_id=s))
        # print new_channel.show
    new_channel.upvote_count = channel['upvote_count']
    new_channel.downvote_count = channel['downvote_count']
    new_channel.save()

    print '<<' + str(new_channel.pk) +'>>'
