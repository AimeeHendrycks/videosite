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

def populate_m(movie_start):

    #response1 gets all movies, but not all of the movie's info
    movies_dict = {'api_key': settings.FMAKEY, 'start_num':movie_start, 'return_num':250, 'sources':'all', 'platform':'web'}
    response1 = requests.get(('https://api-public.guidebox.com/v1.43/US/{api_key}/movie/all/{start_num}/{return_num}/{sources}/{platform}/').format(**movies_dict))
    response1_dict = response1.json()
    movie_list = response1_dict.get('results')

    #pp.pprint (movie_list) 


    for movie in movie_list:
        print '-----------------'

        #response2 gets all single movie info
        movie_dict = {'api_key': settings.FMAKEY, 'id': movie.get('id')}
        response2 = requests.get(('https://api-public.guidebox.com/v1.43/US/{api_key}/movie/{id}').format(**movie_dict))
        response2_dict = response2.json()
        if response2_dict.get('title') != None:
            new_movie, created = Movie.objects.get_or_create(title=str(unidecode(response2_dict.get('title'))))
            print new_movie.title
            print created
            new_movie.movie_id = movie.get('id')
            new_movie.imdb_id = response2_dict.get('imdb')
            new_movie.release_date = response2_dict.get('release_date')
            new_movie.rating = response2_dict.get('rating')
            new_movie.artwork = response2_dict.get("poster_400x570")
            if  response2_dict.get('overview') != None:
                new_movie.overview = response2_dict.get('overview')

            if response2_dict.get('trailers') != None:
                for trailer in response2_dict.get('trailers').get('web'):
                    new_movie.trailer = trailer.get('embed')
                
            new_movie.save()


        # if response2_dict.get('cast') != None:
        #     for c in response2_dict.get('cast'):
        #         if c.get('name') != None: 
        #             new_actor, created = Actor.objects.get_or_create(name=str(unidecode(c.get('name'))))
        #             new_actor.person_id = c.get('id')
        #             #manytomany field requires the .add to create paired relationships
        #             new_actor.movie.add(new_movie)
        #             if new_actor.name != None:
        #                 new_actor.save()
                

        # if response2_dict.get('directors') != None:
        #     for d in response2_dict.get('directors'):
        #         if d.get('name') != None: 
        #             new_director, created = Director.objects.get_or_create(name=str(unidecode(d.get('name'))))
        #             new_director.person_id = d.get('id')
        #             new_director.movie.add(new_movie)
        #             if new_director.name != None:
        #                 new_director.save()
                  

        # if response2_dict.get('writers') != None:
        #     for w in response2_dict.get('writers'):
        #         if w.get('name') != None: 
        #             new_writer, created = Writer.objects.get_or_create(name=str(unidecode(w.get('name'))))
        #             new_writer.person_id = w.get('id')
        #             new_writer.movie.add(new_movie)
        #             if new_writer.name != None:
        #                 new_writer.save()
               

        if response2_dict.get('free_web_sources') != None:
            for free in response2_dict.get('free_web_sources'):
                new_freesource, created = FreeSource.objects.get_or_create(source_id=free.get('id'))
                new_freesource.display_name = free.get('name')
                new_freesource.source_link = free.get('link')
                new_freesource.movie = new_movie
                new_freesource.save()
            
        if response2_dict.get('tv_everywhere_web_sources') != None:
            for tv in response2_dict.get('tv_everywhere_web_sources'):
                new_tvsource, created = TVSource.objects.get_or_create(source_id=tv.get('id'))
                new_tvsource.display_name = tv.get('name')
                new_tvsource.source_link = tv.get('link')
                new_tvsource.movie = new_movie
                new_tvsource.save()
        if response2_dict.get('subscription_web_sources') != None:
            for sub in response2_dict.get('subscription_web_sources'):
                new_subsource, created = SubSource.objects.get_or_create(source_id=sub.get('id'))
                new_subsource.display_name = sub.get('name')
                new_subsource.source_link = sub.get('link')
                new_subsource.movie = new_movie
                new_subsource.save()

        if response2_dict.get('purchase_web_sources') != None:
            for purch in response2_dict.get('purchase_web_sources'):
                new_purchsource, created = PurchaseSource.objects.get_or_create(source_id=purch.get('id'))
                new_purchsource.display_name = purch.get('name')
                new_purchsource.source_link = purch.get('link')
                new_purchsource.movie = new_movie
                new_purchsource.save()

    return 'complete'
