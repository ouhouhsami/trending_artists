# http://developer.echonest.com/api/v4/artist/profile?api_key=GSSGQUJGXGEUZSQ5R&id=ARH6W4X1187B99274F&bucket=id:musicbrainz&format=json
import musicbrainzngs
import time

from pyechonest import artist
from pyechonest import config

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from artists.models import Artist

config.ECHO_NEST_API_KEY=settings.ECHONEST_API

class Command(BaseCommand):

    def handle(self, *args, **options):
        _artists = Artist.objects.all().filter(born__isnull=True).order_by('?')
        musicbrainzngs.set_useragent("Trending artists", "0.1", "http://127.0.0.1:8000")
        for _artist in _artists:
            a = artist.Artist(_artist.echonest_id)
            try:
                musicbrainz_id = a.get_foreign_id().split(':')[2]
                artist_musicbrainz = musicbrainzngs.get_artist_by_id(musicbrainz_id)
                try:
                    print artist_musicbrainz['artist']['life-span']
                    if artist_musicbrainz['artist']['life-span'].get('begin', None):
                        born = artist_musicbrainz['artist']['life-span'].get('begin')
                        if len(born) == 4:
                            born = '%s-01-01' % born
                        elif len(born) == 7:
                            born = '%s-01' % born
                        _artist.born = born
                    if artist_musicbrainz['artist']['life-span'].get('end', None):
                        death = artist_musicbrainz['artist']['life-span'].get('end')
                        if len(death) == 4:
                            death = '%s-01-01' % death
                        elif len(death) == 7:
                            death = '%s-01' % death
                        _artist.death = death
                    _artist.save()
                except:
                    print 'no dates'
            except:
                print 'no musicbrainz'
            time.sleep(4)
            #from pprint import pprint
            #pprint(a)
        self.stdout.write('End')
