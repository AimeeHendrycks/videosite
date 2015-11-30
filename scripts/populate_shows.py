#!/usr/bin/env python
import requests, sys, os, pprint, json

sys.path.append("..")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()
from django.conf import settings
from main.models import Show, Episode, Channel, FreeSource, TVSource, SubSource, PurchaseSource, Person, Actor, Writer, Director
pp = pprint.PrettyPrinter(indent=2)
from unidecode import unidecode


#SHOWS
def populate_s(show_start):
    #response1 gets all movies, but not all of the movie's info
    shows_dict = {'api_key': settings.FMAKEY, 'channel': 'all','start_num':show_start, 'return_num':250, 'sources':'all', 'platform':'web'}
    response1 = requests.get(('https://api-public.guidebox.com/v1.43/US/{api_key}/shows/{channel}/{start_num}/{return_num}/{sources}/{platform}/').format(**shows_dict))
    response1_dict = response1.json()

    show_list = response1_dict.get('results')

    #pp.pprint (show_list) 

    for show in show_list:
        #SHOW
        print '-----------------'
        print show.get('id')

        #response2 gets all single movie info
        show_dict = {'api_key': settings.FMAKEY, 'id': show.get('id')}
        response2 = requests.get(('https://api-public.guidebox.com/v1.43/US/{api_key}/show/{id}').format(**show_dict))
        response2_dict = response2.json()
        if response2_dict.get('title') != None:
            if response2_dict.get('title') != None: 
                new_show, created = Show.objects.get_or_create(title=str(unidecode(response2_dict.get('title'))))
            
                print new_show.title
                print created
                new_show.show_id = show.get('id')
                new_show.status = show.get('status')

                new_show.imdb_id = response2_dict.get('imdb_id')
                new_show.first_aired = response2_dict.get('first_aired')
                new_show.rating = response2_dict.get('rating')
                new_show.artwork = response2_dict.get("poster")
                if response2_dict.get('overview') != None: 
                    new_show.overview = str(unidecode(response2_dict.get('overview')))
                new_show.runtime = response2_dict.get('runtime')
                
                new_show.save()


            if response2_dict.get('channels') != None:
                for chan in response2_dict.get('channels'):
                    new_channel, created = Channel.objects.get_or_create(channel_id=chan.get('id'))
                    new_channel.title = chan.get('name')
                    new_channel.artwork = chan.get('artwork_448x252')
                    new_channel.show.add(new_show)
                    new_channel.save()
            #people
            if response2_dict.get('cast') != None:
                for c in response2_dict.get('cast'):
                    if c.get('name') != None:
                        new_actor, created = Actor.objects.get_or_create(name=str(unidecode(c.get('name'))))
                    
                        new_actor.person_id = c.get('id')
                        new_actor.show.add(new_show)
                        if new_actor.name != None:
                            new_actor.save()


            #/SHOW

            #EPISODES
            
            

            def episode_pop():
                print 'Populating episodes'
                #response3 gets all of the episodes of the show, but not all episode info
                episodes_dict = {'api_key': settings.FMAKEY, 'id': show.get('id'), 'season':'all', 'start_num':0, 'return_num':100, 'sources':'all', 'platform':'web'}
                response3 = requests.get(('https://api-public.guidebox.com/v1.43/US/{api_key}/show/{id}/episodes/{season}/{start_num}/{return_num}/{sources}/{platform}').format(**episodes_dict))
                response3_dict = response3.json()
                
                episode_list = response3_dict.get('results')

                #pp.pprint (episode_list) 
                if episode_list != None:
                    for episode in episode_list:
                        #EPISODE
                        print '.'
                        #response4 gets all single episode info
                        episode_dict = {'api_key': settings.FMAKEY, 'id': episode.get('id')}
                        response4 = requests.get(('https://api-public.guidebox.com/v1.43/US/{api_key}/episode/{id}').format(**episode_dict))
                        response4_dict = response4.json()
                        new_episode, created = Episode.objects.get_or_create(episode_id=response4_dict.get('id'))
                        if episode.get('title') != None:
                            new_episode.title =  str(unidecode(episode.get('title')))
                        
                            new_episode.imdb_id = response4_dict.get('imdb_id')
                            new_episode.season_number = response4_dict.get('season_number')
                            new_episode.episode_number = response4_dict.get('episode_number')
                            new_episode.first_aired = response4_dict.get('first_aired')
                            new_episode.show = new_show
                            new_episode.artwork = response4_dict.get("thumbnail_400x225")
                            if response4_dict.get('overview') != None: 
                                new_episode.overview = str(unidecode(response4_dict.get('overview')))
                            

                            new_episode.save()
                        #people
                        if response4_dict.get('cast') != None:
                            for c in response4_dict.get('cast'):
                                if c.get('name') != None: 
                                    new_actor, created = Actor.objects.get_or_create(name=str(unidecode(c.get('name'))))
                                
                                    new_actor.person_id = c.get('id')
                                    new_actor.episode.add(new_episode)
                                    if new_actor.name != None:
                                        new_actor.save()
                                    

                        if response4_dict.get('directors') != None:
                            for d in response4_dict.get('directors'):
                                if d.get('name') != None: 
                                    new_director, created = Director.objects.get_or_create(name=str(unidecode(d.get('name'))))
                                
                                    new_director.person_id = d.get('id')
                                    new_director.episode.add(new_episode)
                                    if new_director.name != None:
                                        new_director.save()
                                

                        if response4_dict.get('writers') != None:
                            for w in response4_dict.get('writers'):
                                if w.get('name') != None: 
                                    new_writer, created = Writer.objects.get_or_create(name=str(unidecode(w.get('name'))))
                                
                                    new_writer.person_id = w.get('id')
                                    new_writer.episode.add(new_episode)
                                    if new_writer.name != None:
                                        new_writer.save()
                                

                        #watch sources
                        if response4_dict.get('free_web_sources') != None:
                            for free in response4_dict.get('free_web_sources'):
                                new_freesource, created = FreeSource.objects.get_or_create(source_id=free.get('id'))
                                new_freesource.display_name = free.get('name')
                                new_freesource.source_link = free.get('link')
                                new_freesource.episode = new_episode
                                new_freesource.save()
                            
                        if response4_dict.get('tv_everywhere_web_sources') != None:
                            for tv in response4_dict.get('tv_everywhere_web_sources'):
                                new_tvsource, created = TVSource.objects.get_or_create(source_id=tv.get('id'))
                                new_tvsource.display_name = tv.get('name')
                                new_tvsource.source_link = tv.get('link')
                                new_tvsource.episode = new_episode
                                new_tvsource.save()

                        if response4_dict.get('subscription_web_sources') != None:
                            for sub in response4_dict.get('subscription_web_sources'):
                                new_subsource, created = SubSource.objects.get_or_create(source_id=sub.get('id'))
                                new_subsource.display_name = sub.get('name')
                                new_subsource.source_link = sub.get('link')
                                new_subsource.episode = new_episode
                                new_subsource.save()

                        if response4_dict.get('purchase_web_sources') != None:
                            for purch in response4_dict.get('purchase_web_sources'):
                                new_purchsource, created = PurchaseSource.objects.get_or_create(source_id=purch.get('id'))
                                new_purchsource.display_name = purch.get('name')
                                new_purchsource.source_link = purch.get('link')
                                new_purchsource.episode = new_episode
                                new_purchsource.save()
            try:
                try:
                    episode_pop()
                except:
                    episode_pop()
            except:
                try:
                    episode_pop()
                except:
                    episode_pop()



    return 'complete'
