from __future__ import absolute_import

import time

from django.conf import settings

from pyechonest import artist
from pyechonest import config

from trending_artists.celery import app
from .models import Artist, Trend


@app.task
def trend():
    config.ECHO_NEST_API_KEY=settings.ECHONEST_API
    for a in Artist.objects.all():
        # 3 echonest api calls 
        artist_ = artist.Artist(a.echonest_id)
        familiarity = artist_.get_familiarity(cache=False)
        hotttnesss = artist_.get_hotttnesss(cache=False)
        trend = Trend(artist=a, familiarity=familiarity, hotttnesss=hotttnesss)
        trend.save()
        time.sleep(60/5)

