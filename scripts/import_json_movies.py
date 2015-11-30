#!/usr/bin/env python
import sys, os, pprint, json
sys.path.append("..")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
from unidecode import unidecode

import django
django.setup()
from django.conf import settings
from main.models import Movie

with open('movie_json.txt') as data_file:
    data = json.load(data_file)

# print data
for movie in data:
    new_movie, created = Movie.objects.get_or_create(movie_id=movie['movie_id'])
    print new_movie.movie_id
    print '<<' + new_movie.pk +'>>'
    new_movie.title = str(unidecode(movie['title']))
    print new_movie.title
    new_movie.imdb_id = movie['imdb_id']
    new_movie.release_date = movie['release_date']
    new_movie.rating = movie['rating']
    new_movie.artwork = movie['artwork']
    new_movie.overview = str(unidecode(movie['overview']))
    new_movie.trailer = movie['trailer']
    new_movie.upvote_count = movie['upvote_count']
    new_movie.downvote_count = movie['downvote_count']
    new_movie.save()
    print '<<' + new_movie.pk +'>>'
