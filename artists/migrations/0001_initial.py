# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Artist'
        db.create_table(u'artists_artist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('echonest_id', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'artists', ['Artist'])

        # Adding model 'Trend'
        db.create_table(u'artists_trend', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['artists.Artist'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('familiarity', self.gf('django.db.models.fields.FloatField')()),
            ('hotttnesss', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'artists', ['Trend'])


    def backwards(self, orm):
        # Deleting model 'Artist'
        db.delete_table(u'artists_artist')

        # Deleting model 'Trend'
        db.delete_table(u'artists_trend')


    models = {
        u'artists.artist': {
            'Meta': {'object_name': 'Artist'},
            'echonest_id': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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