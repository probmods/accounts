# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Saved_code'
        db.create_table(u'user_code_saved_code', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user_code.User_code'])),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['custom_user.EmailUser'])),
            ('exercise_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user_code.Exercise'])),
            ('forest_errors', self.gf('django.db.models.fields.TextField')()),
            ('forest_plots', self.gf('django.db.models.fields.TextField')()),
            ('forest_results', self.gf('django.db.models.fields.TextField')()),
            ('date_saved', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'user_code', ['Saved_code'])


    def backwards(self, orm):
        # Deleting model 'Saved_code'
        db.delete_table(u'user_code_saved_code')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'custom_user.emailuser': {
            'Meta': {'object_name': 'EmailUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'user_code.exercise': {
            'Meta': {'object_name': 'Exercise'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'user_code.saved_code': {
            'Meta': {'object_name': 'Saved_code'},
            'code_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user_code.User_code']"}),
            'date_saved': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exercise_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user_code.Exercise']"}),
            'forest_errors': ('django.db.models.fields.TextField', [], {}),
            'forest_plots': ('django.db.models.fields.TextField', [], {}),
            'forest_results': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['custom_user.EmailUser']"})
        },
        u'user_code.user_code': {
            'Meta': {'object_name': 'User_code'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exercise_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user_code.Exercise']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['custom_user.EmailUser']"})
        }
    }

    complete_apps = ['user_code']