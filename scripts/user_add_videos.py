#!/usr/bin/env python
def add_movie(movie):
    request.user.movie.add(movie)

def add_show(show):
    request.user.show.add(show)

def add_episode(ep):
    request.user.episode.add(ep)