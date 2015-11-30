#!/usr/bin/env python
import json

with open('movie_json.txt') as data_file:
    data = json.load(data_file)

print data
for movie in data:
    new_movie, created = Movie.objects.get_or_create(movie_id=str(unidecode(movie['movie_id'])))
    new_movie.title = movie['title']
    new_movie.imdb_id = movie['imdb_id']
    new_movie.release_date = movie['release_date']
    new_movie.rating = movie['rating']
    new_movie.artwork = movie['artwork']
    new_movie.overview = movie['overview']
    new_movie.trailer = movie['trailer']
    new_movie.upvote_count = movie['upvote_count']
    new_movie.downvote_count = movie['downvote_count']
    new_movie.save()
