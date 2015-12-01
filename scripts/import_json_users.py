#!/usr/bin/env python
import sys, os, pprint, json
sys.path.append("..")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
from unidecode import unidecode

import django
django.setup()
from django.conf import settings
from main.models import Color, CustomUser

with open('color_json.txt') as data_file:
    data = json.load(data_file)

# print data
for color in data:
    new_color, created = Color.objects.get_or_create(title=color['title'])
    print new_color.hex_value
    
    new_color.hex_value = color['hex_value']
    
    new_color.save()

    print '<<' + str(new_color.pk) +'>>'




with open('user_json.txt') as data_file:
    data = json.load(data_file)

# print data
for user in data:
    new_user, created = CustomUser.objects.get_or_create(email=user['email'])
    print new_user.email
    if user['account_name'] != None:
        new_user.account_name = str(unidecode(user['account_name']))
        print new_user.account_name
    
    new_user.account_color = user['account_color']
    new_user.account_picture = user['account_picture']
    new_user.is_staff = user['is_staff']
    new_user.is_active = user['is_active']
    for s in user['shows']:
        print str(s) + ' show'
        new_user.show.add(Show.objects.get(show_id=s))
    for m in user['movies']:
        print str(m) + ' movie'
        new_user.movie.add(Movie.objects.get(movie_id=m))
    
    new_user.save()

    print '<<' + str(new_user.pk) +'>>'
