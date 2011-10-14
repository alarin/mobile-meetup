# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MenuItemExt'
        db.create_table('anticms_menuitemext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('menu_item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ext', to=orm['treemenus.MenuItem'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbtemplates.Template'], null=True, blank=True)),
        ))
        db.send_create_signal('anticms', ['MenuItemExt'])

        # Adding unique constraint on 'MenuItemExt', fields ['menu_item', 'language']
        db.create_unique('anticms_menuitemext', ['menu_item_id', 'language'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'MenuItemExt', fields ['menu_item', 'language']
        db.delete_unique('anticms_menuitemext', ['menu_item_id', 'language'])

        # Deleting model 'MenuItemExt'
        db.delete_table('anticms_menuitemext')


    models = {
        'anticms.menuitemext': {
            'Meta': {'ordering': "('menu_item__rank',)", 'unique_together': "(('menu_item', 'language'),)", 'object_name': 'MenuItemExt'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'menu_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ext'", 'to': "orm['treemenus.MenuItem']"}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbtemplates.Template']", 'null': 'True', 'blank': 'True'})
        },
        'dbtemplates.template': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Template', 'db_table': "'django_template'"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_changed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'treemenus.menu': {
            'Meta': {'object_name': 'Menu'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'root_item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'is_root_item_of'", 'null': 'True', 'to': "orm['treemenus.MenuItem']"})
        },
        'treemenus.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contained_items'", 'null': 'True', 'to': "orm['treemenus.Menu']"}),
            'named_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['treemenus.MenuItem']", 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['anticms']
