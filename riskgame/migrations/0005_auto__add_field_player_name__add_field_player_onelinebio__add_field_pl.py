# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Player.name'
        db.add_column(u'riskgame_player', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'Player.onelinebio'
        db.add_column(u'riskgame_player', 'onelinebio',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=140),
                      keep_default=False)

        # Adding field 'Player.role'
        db.add_column(u'riskgame_player', 'role',
                      self.gf('django.db.models.fields.CharField')(default='OFFICE', max_length=255),
                      keep_default=False)

        # Adding field 'Player.receive_email'
        db.add_column(u'riskgame_player', 'receive_email',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Player.name'
        db.delete_column(u'riskgame_player', 'name')

        # Deleting field 'Player.onelinebio'
        db.delete_column(u'riskgame_player', 'onelinebio')

        # Deleting field 'Player.role'
        db.delete_column(u'riskgame_player', 'role')

        # Deleting field 'Player.receive_email'
        db.delete_column(u'riskgame_player', 'receive_email')


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
            'datestart': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'riskgame.player': {
            'Meta': {'object_name': 'Player'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'onelinebio': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '140'}),
            'receive_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'OFFICE'", 'max_length': '255'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['riskgame.Team']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['riskgame.EmailUser']", 'unique': 'True'})
        },
        u'riskgame.team': {
            'Meta': {'object_name': 'Team'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'goal_zero_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'a'", 'max_length': '255'}),
            'open': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'resource_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'victory_points': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'riskgame.teamjoinrequest': {
            'Meta': {'object_name': 'TeamJoinRequest'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['riskgame.Player']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['riskgame.Team']"})
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