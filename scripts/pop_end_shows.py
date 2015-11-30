#!/usr/bin/env python
from populate_shows import populate_s

# def populate_videos():
    
    # movie:total_results": 71042 -- 284 times
    # show:"total_results": 11081 -- 44

    #start at 10000
for s in range(11250,71042,250):
    try:
        try:
            populate_s(s)
        except:
            populate_s(s)
    except:
        try:
            populate_s(s)
        except:
            populate_s(s)