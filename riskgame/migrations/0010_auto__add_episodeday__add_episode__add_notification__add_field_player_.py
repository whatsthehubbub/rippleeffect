# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EpisodeDay'
        db.create_table(u'riskgame_episodeday', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datecreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('datechanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['riskgame.Episode'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'riskgame', ['EpisodeDay'])

        # Adding model 'Episode'
        db.create_table(u'riskgame_episode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datecreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('datechanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'riskgame', ['Episode'])

        # Adding model 'Notification'
        db.create_table(u'riskgame_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datecreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('datechanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['riskgame.Team'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['riskgame.Player'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'riskgame', ['Notification'])

        # Deleting field 'Game.datestart'
        db.delete_column(u'riskgame_game', 'datestart')

        # Adding field 'Player.emails_unsubscribe_hash'
        db.add_column(u'riskgame_player', 'emails_unsubscribe_hash',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Player.timezone'
        db.add_column(u'riskgame_player', 'timezone',
                      self.gf('timezone_field.fields.TimeZoneField')(default='Europe/Amsterdam'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'EpisodeDay'
        db.delete_table(u'riskgame_episodeday')

        # Deleting model 'Episode'
        db.delete_table(u'riskgame_episode')

        # Deleting model 'Notification'
        db.delete_table(u'riskgame_notification')

        # Adding field 'Game.datestart'
        db.add_column(u'riskgame_game', 'datestart',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 4, 2, 0, 0)),
                      keep_default=False)

        # Deleting field 'Player.emails_unsubscribe_hash'
        db.delete_column(u'riskgame_player', 'emails_unsubscribe_hash')

        # Deleting field 'Player.timezone'
        db.delete_column(u'riskgame_player', 'timezone')


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
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['riskgame.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'riskgame.game': {
            'Meta': {'object_name': 'Game'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'riskgame.notification': {
            'Meta': {'object_name': 'Notification'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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