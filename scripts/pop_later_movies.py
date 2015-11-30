#!/usr/bin/env python
import requests, sys, os, pprint, json

sys.path.append("..")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()
from django.conf import settings
from main.models import Movie, FreeSource, TVSource, SubSource, PurchaseSource, Person, Actor, Writer, Director
pp = pprint.PrettyPrinter(indent=2)
from unidecode import unidecode


for movie in Movie.objects.all():
    print '-----------------'

    #response2 gets all single movie info
    movie_dict = {'api_key': settings.FMAKEY, 'id': movie.movie_id}
    response2 = requests.get(('https://api-public.guidebox.com/v1.43/US/{api_key}/movie/{id}').format(**movie_dict))
    response2_dict = response2.json()
    if response2_dict.get('title') != None:
        a_movie= Movie.objects.get(title=str(unidecode(response2_dict.get('title'))))
        print a_movie.title
        if response2_dict.get('trailers') != None:
            for trailer in response2_dict.get('trailers').get('web'):
                a_movie.trailer = trailer.get('link')
                print a_movie.trailer
            
        a_movie.save()


    if response2_dict.get('free_web_sources') != None:
        for free in response2_dict.get('free_web_sources'):
            new_freesource, created = FreeSource.objects.get_or_create(source_link=free.get('link'))
            new_freesource.display_name = free.get('display_name')
            print new_freesource.display_name
            new_freesource.movie = a_movie
            new_freesource.save()
        
    if response2_dict.get('tv_everywhere_web_sources') != None:
        for tv in response2_dict.get('tv_everywhere_web_sources'):
            new_tvsource, created = TVSource.objects.get_or_create(source_link=tv.get('link'))
            new_tvsource.display_name = tv.get('display_name')
            print new_tvsource.display_name
            new_tvsource.movie = a_movie
            new_tvsource.save()
    if response2_dict.get('subscription_web_sources') != None:
        for sub in response2_dict.get('subscription_web_sources'):
            new_subsource, created = SubSource.objects.get_or_create(source_link=sub.get('link'))
            new_subsource.display_name = sub.get('display_name')
            print new_subsource.display_name
            new_subsource.movie = a_movie
            new_subsource.save()

    if response2_dict.get('purchase_web_sources') != None:
        for purch in response2_dict.get('purchase_web_sources'):
            new_purchsource, created = PurchaseSource.objects.get_or_create(source_link=purch.get('link'))
            new_purchsource.display_name = purch.get('display_name')
            print new_purchsource.display_name
            new_purchsource.movie = a_movie
            new_purchsource.save()

