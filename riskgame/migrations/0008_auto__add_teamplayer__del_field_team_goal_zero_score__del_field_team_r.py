# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TeamPlayer'
        db.create_table(u'riskgame_teamplayer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datecreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('datechanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(default='office', max_length=255)),
            ('gather_pile', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default='', max_length=255)),
            ('gather_markers', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('risk_pile', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default='', max_length=255)),
            ('prevent_markers', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['riskgame.Team'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['riskgame.Player'])),
        ))
        db.send_create_signal(u'riskgame', ['TeamPlayer'])

        # Deleting field 'Team.goal_zero_score'
        db.delete_column(u'riskgame_team', 'goal_zero_score')

        # Deleting field 'Team.resource_score'
        db.delete_column(u'riskgame_team', 'resource_score')

        # Deleting field 'Team.victory_points'
        db.delete_column(u'riskgame_team', 'victory_points')

        # Adding field 'Team.goal_zero_markers'
        db.add_column(u'riskgame_team', 'goal_zero_markers',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Team.action_points'
        db.add_column(u'riskgame_team', 'action_points',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Team.score'
        db.add_column(u'riskgame_team', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Player.team'
        db.delete_column(u'riskgame_player', 'team_id')


    def backwards(self, orm):
        # Deleting model 'TeamPlayer'
        db.delete_table(u'riskgame_teamplayer')

        # Adding field 'Team.goal_zero_score'
        db.add_column(u'riskgame_team', 'goal_zero_score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Team.resource_score'
        db.add_column(u'riskgame_team', 'resource_score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Team.victory_points'
        db.add_column(u'riskgame_team', 'victory_points',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Team.goal_zero_markers'
        db.delete_column(u'riskgame_team', 'goal_zero_markers')

        # Deleting field 'Team.action_points'
        db.delete_column(u'riskgame_team', 'action_points')

        # Deleting field 'Team.score'
        db.delete_column(u'riskgame_team', 'score')

        # Adding field 'Player.team'
        db.add_column(u'riskgame_player', 'team',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['riskgame.Team'], null=True, blank=True),
                      keep_default=False)


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
            'gather_pile': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['riskgame.Player']"}),
            'prevent_markers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'risk_pile': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '255'}),
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