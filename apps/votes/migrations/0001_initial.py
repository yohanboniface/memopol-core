# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Proposal'
        db.create_table('votes_proposal', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=63, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('votes', ['Proposal'])

        # Adding model 'Recommendation'
        db.create_table('votes_recommendation', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=511)),
            ('weight', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('part', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('recommendation', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('proposal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['votes.Proposal'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('votes', ['Recommendation'])

        # Adding model 'Vote'
        db.create_table('votes_vote', (
            ('recommendation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['votes.Recommendation'])),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.Representative'], null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('choice', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('votes', ['Vote'])

        # Adding model 'Score'
        db.create_table('votes_score', (
            ('proposal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['votes.Proposal'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.Representative'])),
        ))
        db.send_create_signal('votes', ['Score'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Proposal'
        db.delete_table('votes_proposal')

        # Deleting model 'Recommendation'
        db.delete_table('votes_recommendation')

        # Deleting model 'Vote'
        db.delete_table('votes_vote')

        # Deleting model 'Score'
        db.delete_table('votes_score')
    
    
    models = {
        'reps.opinion': {
            'Meta': {'object_name': 'Opinion'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1023'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'reps.opinionrep': {
            'Meta': {'object_name': 'OpinionREP'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opinion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Opinion']"}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"})
        },
        'reps.party': {
            'Meta': {'object_name': 'Party'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'reps.partyrepresentative': {
            'Meta': {'object_name': 'PartyRepresentative'},
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Party']"}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'reps.representative': {
            'Meta': {'object_name': 'Representative'},
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'local_party': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reps.Party']", 'through': "orm['reps.PartyRepresentative']", 'symmetrical': 'False'}),
            'opinions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reps.Opinion']", 'through': "orm['reps.OpinionREP']", 'symmetrical': 'False'}),
            'picture': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'votes.proposal': {
            'Meta': {'object_name': 'Proposal'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '63', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'votes.recommendation': {
            'Meta': {'object_name': 'Recommendation'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '511'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['votes.Proposal']"}),
            'recommendation': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'votes.score': {
            'Meta': {'object_name': 'Score'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['votes.Proposal']"}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'votes.vote': {
            'Meta': {'object_name': 'Vote'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'recommendation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['votes.Recommendation']"}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']", 'null': 'True'})
        }
    }
    
    complete_apps = ['votes']
