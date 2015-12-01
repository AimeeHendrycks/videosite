#!/usr/bin/env python
import sys, os, pprint, json
sys.path.append("..")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
from unidecode import unidecode

import django
django.setup()
from django.conf import settings
from main.models import Comment, Reply, Response, CustomUser, Movie, Show, Episode, Channel

with open('comment_json.txt') as data_file:
    data = json.load(data_file)

print data
for comment in data:
    if comment['date_created'] != '':
        new_comment, created = Comment.objects.get_or_create(date=comment['date_created'])
        print 'comment made'
        new_comment.text = comment['text']
        print new_comment.text
        new_comment.is_reply = comment['is_reply']
        print new_comment.is_reply
        new_comment.user = CustomUser.objects.get(email=comment['user'])
        print new_comment.user
        if comment['comment_type'] == 'movie':
            new_comment.movie = Movie.objects.get(pk=comment['movie'])
            print new_comment.movie
        if comment['comment_type'] == 'show':
            new_comment.show = Show.objects.get(pk=comment['show'])
            print new_comment.show
        if comment['comment_type'] == 'episode':
            new_comment.episode = Episode.objects.get(pk=comment['episode'])
            print new_comment.episode
        if comment['comment_type'] == 'channel':
            new_comment.channel = Channel.objects.get(pk=comment['channel'])
            print new_comment.channel
        # new_comment.save()

        print '<<' + str(new_comment.pk) +'>>'
        print '.............'


with open('response_json.txt') as data_file:
    data = json.load(data_file)
print '-----------'
print data

for response in data:
    if response['date_created'] != '':
        new_response, created = Response.objects.get_or_create(date=response['date_created'])
        new_response.text = response['text']
        print new_response.text
        new_response.is_resp_to_reply = response['is_resp_to_reply']
        print new_response.is_resp_to_reply
        new_response.original_comment = Comment.objects.get(date=response['original_comment'])
        print new_response.original_comment
        new_response.user = CustomUser.objects.get(email=response['user'])
        print new_response.user
        if response['response_type'] == 'movie':
            new_response.movie = Movie.objects.get(pk=response['movie'])
            print new_response.movie
        if response['response_type'] == 'show':
            new_response.show = Show.objects.get(pk=response['show'])
            print new_response.show
        if response['response_type'] == 'episode':
            new_response.episode = Episode.objects.get(pk=response['episode'])
            print new_response.episode
        if response['response_type'] == 'channel':
            new_response.channel = Channel.objects.get(pk=response['channel'])
            print new_response.channel
        # new_response.save()

        print '<<' + str(new_response.pk) +'>>'
        print '.............'



with open('reply_json.txt') as data_file:
    data = json.load(data_file)
print '-------------'
print data

for reply in data:
    if reply['date_created'] != '':
        new_reply, created = Reply.objects.get_or_create(date=reply['date_created'])
        new_reply.text = reply['text']
        print new_reply.text
        new_reply.original_response = Response.objects.get(date=reply['original_response'])
        print new_reply.original_response
        new_reply.copy, created = Comment.objects.get_or_create(date=reply['date_created'])
        print new_reply.copy
        new_reply.user = CustomUser.objects.get(email=reply['user'])
        print new_reply.user
        if reply['reply_type'] == 'movie':
            new_reply.movie = Movie.objects.get(pk=reply['movie'])
            print new_reply.movie
        if reply['reply_type'] == 'show':
            new_reply.show = Show.objects.get(pk=reply['show'])
            print new_reply.show
        if reply['reply_type'] == 'episode':
            new_reply.episode = Episode.objects.get(pk=reply['episode'])
            print new_reply.episode
        if reply['reply_type'] == 'channel':
            new_reply.channel = Channel.objects.get(pk=reply['channel'])
            print new_reply.channel
        # new_reply.save()

        print '<<' + str(new_reply.pk) +'>>'
        print '.............'

