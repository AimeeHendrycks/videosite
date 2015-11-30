#!/usr/bin/env python
from populate_movies import populate_m

for m in range(0,11081,250):
    try:
        try:
            populate_m(m)
        except:
            populate_m(m)
    except:
        try:
            populate_m(m)
        except:
            populate_m(m)