# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for artist in orm['artists.Artist'].objects.all():
            if artist.festivals:
                years = artist.festivals.split(',')
                for year in years:
                    year = int(year)
                    try:
                        festival = orm['artists.Festival'].objects.get(year=year)
                    except orm['artists.Festival'].DoesNotExist:
                        festival = orm['artists.Festival'](year=year)
                        festival.save()
                    festival.artists.add(artist)

    def backwards(self, orm):
        "Write your backwards methods here."
        pass

    models = {
        u'artists.artist': {
            'Meta': {'object_name': 'Artist'},
            'echonest_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'festivals': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'guest_artist': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'artists.festival': {
            'Meta': {'object_name': 'Festival'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'festival'", 'symmetrical': 'False', 'to': u"orm['artists.Artist']"}),
            'guest_artists': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'festival_guest'", 'symmetrical': 'False', 'to': u"orm['artists.Artist']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'artists.trend': {
            'Meta': {'object_name': 'Trend'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['artists.Artist']"}),
            'familiarity': ('django.db.models.fields.FloatField', [], {}),
            'hotttnesss': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['artists']
    symmetrical = True
