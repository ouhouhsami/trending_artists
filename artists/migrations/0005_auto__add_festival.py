# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Festival'
        db.create_table(u'artists_festival', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'artists', ['Festival'])

        # Adding M2M table for field guest_artists on 'Festival'
        m2m_table_name = db.shorten_name(u'artists_festival_guest_artists')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('festival', models.ForeignKey(orm[u'artists.festival'], null=False)),
            ('artist', models.ForeignKey(orm[u'artists.artist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['festival_id', 'artist_id'])

        # Adding M2M table for field artists on 'Festival'
        m2m_table_name = db.shorten_name(u'artists_festival_artists')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('festival', models.ForeignKey(orm[u'artists.festival'], null=False)),
            ('artist', models.ForeignKey(orm[u'artists.artist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['festival_id', 'artist_id'])


    def backwards(self, orm):
        # Deleting model 'Festival'
        db.delete_table(u'artists_festival')

        # Removing M2M table for field guest_artists on 'Festival'
        db.delete_table(db.shorten_name(u'artists_festival_guest_artists'))

        # Removing M2M table for field artists on 'Festival'
        db.delete_table(db.shorten_name(u'artists_festival_artists'))


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