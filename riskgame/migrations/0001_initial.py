# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailUser'
        db.create_table(u'riskgame_emailuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255, db_index=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'riskgame', ['EmailUser'])

        # Adding model 'ValidEmailDomain'
        db.create_table(u'riskgame_validemaildomain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datecreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('datechanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'riskgame', ['ValidEmailDomain'])

        # Adding model 'Game'
        db.create_table(u'riskgame_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datecreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('datechanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('started', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'riskgame', ['Game'])


    def backwards(self, orm):
        # Deleting model 'EmailUser'
        db.delete_table(u'riskgame_emailuser')

        # Deleting model 'ValidEmailDomain'
        db.delete_table(u'riskgame_validemaildomain')

        # Deleting model 'Game'
        db.delete_table(u'riskgame_game')


    models = {
        u'riskgame.emailuser': {
            'Meta': {'object_name': 'EmailUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'riskgame.game': {
            'Meta': {'object_name': 'Game'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'started': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'riskgame.validemaildomain': {
            'Meta': {'object_name': 'ValidEmailDomain'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['riskgame']