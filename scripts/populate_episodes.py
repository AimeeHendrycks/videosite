#!/usr/bin/env python
import requests, sys, os, pprint, json

sys.path.append("..")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()
from django.conf import settings

from main.models import Episode, FreeSource, TVSource, SubSource, PurchaseSource, Person, Actor, Writer, Director

    
for episode in Episode.objects.all()[50800:]:
    if episode.videosource_set.all().count() == 0:
        episode_dict = {'api_key': settings.FMAKEY, 'id': episode.episode_id}
        response2 = requests.get(('https://api-public.guidebox.com/v1.43/US/{api_key}/episode/{id}').format(**episode_dict))
        response2_dict = response2.json()
        an_episode= Episode.objects.get(episode_id=response2_dict.get('id'))
        print an_episode.title
        print an_episode.pk
                #watch sources
        if response2_dict.get('free_web_sources') != None:
            for free in response2_dict.get('free_web_sources'):
                new_freesource, created = FreeSource.objects.get_or_create(source_link=free.get('link'))
                new_freesource.display_name = free.get('display_name')
                print new_freesource.display_name
                new_freesource.episode = an_episode
                new_freesource.save()
            
        if response2_dict.get('tv_everywhere_web_sources') != None:
            for tv in response2_dict.get('tv_everywhere_web_sources'):
                new_tvsource, created = TVSource.objects.get_or_create(source_link=tv.get('link'))
                new_tvsource.display_name = tv.get('display_name')
                print new_tvsource.display_name
                new_tvsource.episode = an_episode
                new_tvsource.save()
        if response2_dict.get('subscription_web_sources') != None:
            for sub in response2_dict.get('subscription_web_sources'):
                new_subsource, created = SubSource.objects.get_or_create(source_link=sub.get('link'))
                new_subsource.display_name = sub.get('display_name')
                print new_subsource.display_name
                new_subsource.episode = an_episode
                new_subsource.save()

        if response2_dict.get('purchase_web_sources') != None:
            for purch in response2_dict.get('purchase_web_sources'):
                new_purchsource, created = PurchaseSource.objects.get_or_create(source_link=purch.get('link'))
                new_purchsource.display_name = purch.get('display_name')
                print new_purchsource.display_name
                new_purchsource.episode = an_episode
                new_purchsource.save()