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

# print data
for comment in data:
    if comment['date_created'] != '':
        new_comment, created = Comment.objects.get_or_create(date=comment['date_created'])
        new_comment.text = comment['text']
        print new_comment.text
        new_comment.is_reply = comment['is_reply']
        print new_comment.is_reply
        new_comment.user = CustomUser.objects.get(pk=comment['user'])
        print new_comment.user
        new_comment.movie = Movie.objects.get(pk=comment['movie'])
        print new_comment.movie
        new_comment.show = Show.objects.get(pk=comment['show'])
        print new_comment.show
        new_comment.episode = Episode.objects.get(pk=comment['episode'])
        print new_comment.episode
        new_comment.channel = Channel.objects.get(pk=comment['channel'])
        print new_comment.channel
        # new_comment.save()

        print '<<' + str(new_comment.pk) +'>>'


with open('response_json.txt') as data_file:
    data = json.load(data_file)

# print data
for response in data:
    if response['date_created'] != '':
        new_response, created = Response.objects.get_or_create(date=response['date_created'])
        new_response.text = response['text']
        print new_response.text
        new_response.is_resp_to_reply = response['is_resp_to_reply']
        print new_response.is_resp_to_reply
        new_response.original_comment = Comment.objects.get(pk=response['original_comment'])
        print new_response.original_comment
        new_response.user = CustomUser.objects.get(pk=response['user'])
        print new_response.user
        new_response.movie = Movie.objects.get(pk=response['movie'])
        print new_response.movie
        new_response.show = Show.objects.get(pk=response['show'])
        print new_response.show
        new_response.episode = Episode.objects.get(pk=response['episode'])
        print new_response.episode
        new_response.channel = Channel.objects.get(pk=response['channel'])
        print new_response.channel
        # new_response.save()

        print '<<' + str(new_response.pk) +'>>'



with open('reply_json.txt') as data_file:
    data = json.load(data_file)

# print data
for reply in data:
    if reply['date_created'] != '':
        new_reply, created = Reply.objects.get_or_create(date=reply['date_created'])
        new_reply.text = reply['text']
        print new_reply.text
        new_reply.original_response = Response.objects.get(pk=reply['original_response'])
        print new_reply.original_response
        new_reply.copy, created = Comment.objects.get_or_create(date=reply['date_created'])
        print new_reply.copy.text
        new_reply.user = CustomUser.objects.get(pk=reply['user'])
        print new_reply.user
        new_reply.movie = Movie.objects.get(pk=reply['movie'])
        print new_reply.movie
        new_reply.show = Show.objects.get(pk=reply['show'])
        print new_reply.show
        new_reply.episode = Episode.objects.get(pk=reply['episode'])
        print new_reply.episode
        new_reply.channel = Channel.objects.get(pk=reply['channel'])
        print new_reply.channel
        # new_reply.save()

        print '<<' + str(new_reply.pk) +'>>'

