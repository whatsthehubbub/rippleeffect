# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Game.start'
        db.add_column(u'riskgame_game', 'start',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 4, 3, 0, 0)),
                      keep_default=False)

        # Deleting field 'EpisodeDay.start'
        db.delete_column(u'riskgame_episodeday', 'start')

        # Adding field 'EpisodeDay.end'
        db.add_column(u'riskgame_episodeday', 'end',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 4, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Team.currentDay'
        db.add_column(u'riskgame_team', 'currentDay',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['riskgame.EpisodeDay'], null=True),
                      keep_default=False)

        # Adding field 'Team.check_next'
        db.add_column(u'riskgame_team', 'check_next',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Notification.email'
        db.add_column(u'riskgame_notification', 'email',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Game.start'
        db.delete_column(u'riskgame_game', 'start')

        # Adding field 'EpisodeDay.start'
        db.add_column(u'riskgame_episodeday', 'start',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 4, 3, 0, 0)),
                      keep_default=False)

        # Deleting field 'EpisodeDay.end'
        db.delete_column(u'riskgame_episodeday', 'end')

        # Deleting field 'Team.currentDay'
        db.delete_column(u'riskgame_team', 'currentDay_id')

        # Deleting field 'Team.check_next'
        db.delete_column(u'riskgame_team', 'check_next')

        # Deleting field 'Notification.email'
        db.delete_column(u'riskgame_notification', 'email')


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
        u'riskgame.episode': {
            'Meta': {'object_name': 'Episode'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'riskgame.episodeday': {
            'Meta': {'object_name': 'EpisodeDay'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['riskgame.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'riskgame.game': {
            'Meta': {'object_name': 'Game'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'riskgame.notification': {
            'Meta': {'object_name': 'Notification'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['riskgame.Player']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['riskgame.Team']"})
        },
        u'riskgame.player': {
            'Meta': {'object_name': 'Player'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'emails_unsubscribe_hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'onelinebio': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '140', 'blank': 'True'}),
            'receive_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {'default': "'Europe/Amsterdam'"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['riskgame.EmailUser']", 'unique': 'True'})
        },
        u'riskgame.team': {
            'Meta': {'object_name': 'Team'},
            'action_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'check_next': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'currentDay': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['riskgame.EpisodeDay']", 'null': 'True'}),
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'goal_zero_markers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leader': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ledteam'", 'null': 'True', 'to': u"orm['riskgame.Player']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'open': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['riskgame.Player']", 'through': u"orm['riskgame.TeamPlayer']", 'symmetrical': 'False'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'riskgame.teamjoinrequest': {
            'Meta': {'object_name': 'TeamJoinRequest'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['riskgame.Player']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['riskgame.Team']"})
        },
        u'riskgame.teamplayer': {
            'Meta': {'object_name': 'TeamPlayer'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gather_markers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'gather_pile': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['riskgame.Player']"}),
            'prevent_markers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'risk_pile': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'office'", 'max_length': '255'}),
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