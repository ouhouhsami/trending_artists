# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Artist.festivals'
        db.delete_column(u'artists_artist', 'festivals')

        # Deleting field 'Artist.guest_artist'
        db.delete_column(u'artists_artist', 'guest_artist')


    def backwards(self, orm):
        # Adding field 'Artist.festivals'
        db.add_column(u'artists_artist', 'festivals',
                      self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Artist.guest_artist'
        db.add_column(u'artists_artist', 'guest_artist',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        u'artists.artist': {
            'Meta': {'object_name': 'Artist'},
            'echonest_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
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