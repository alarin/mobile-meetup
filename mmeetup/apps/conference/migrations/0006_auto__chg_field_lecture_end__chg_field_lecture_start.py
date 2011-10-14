# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Lecture.end'
        db.alter_column('conference_lecture', 'end', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Lecture.start'
        db.alter_column('conference_lecture', 'start', self.gf('django.db.models.fields.DateTimeField')(null=True))


    def backwards(self, orm):
        
        # Changing field 'Lecture.end'
        db.alter_column('conference_lecture', 'end', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2011, 10, 9, 21, 53, 56, 517613)))

        # Changing field 'Lecture.start'
        db.alter_column('conference_lecture', 'start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 10, 9, 21, 54, 5, 308563)))


    models = {
        'conference.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'conference.lecture': {
            'Meta': {'ordering': "('start',)", 'object_name': 'Lecture'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_brake': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Speaker']", 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'conference.partner': {
            'Meta': {'object_name': 'Partner'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.PartnerSection']", 'null': 'True', 'blank': 'True'})
        },
        'conference.partnersection': {
            'Meta': {'object_name': 'PartnerSection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'conference.speaker': {
            'Meta': {'object_name': 'Speaker'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Company']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['conference']
