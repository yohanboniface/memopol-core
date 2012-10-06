# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'FunctionMP.extra'
        db.delete_column('mps_functionmp', 'extra')

        # Adding field 'FunctionMP.extra_parliamentary'
        db.add_column('mps_functionmp', 'extra_parliamentary', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'FunctionMP.extra'
        db.add_column('mps_functionmp', 'extra', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'FunctionMP.extra_parliamentary'
        db.delete_column('mps_functionmp', 'extra_parliamentary')


    models = {
        'mps.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps.MP']"}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True'})
        },
        'mps.canton': {
            'Meta': {'object_name': 'Canton'},
            'circonscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps.Circonscription']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '511'})
        },
        'mps.circonscription': {
            'Meta': {'object_name': 'Circonscription'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps.Department']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '31'})
        },
        'mps.department': {
            'Meta': {'object_name': 'Department'},
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'})
        },
        'mps.function': {
            'Meta': {'object_name': 'Function'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mps.functionmp': {
            'Meta': {'object_name': 'FunctionMP'},
            'extra_parliamentary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps.Function']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'mp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps.MP']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mps.group': {
            'Meta': {'object_name': 'Group'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '31', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mps.mandate': {
            'Meta': {'object_name': 'Mandate'},
            'begin_reason': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'begin_term': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'election_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'end_reason': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'end_term': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'mp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps.MP']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '127'})
        },
        'mps.mp': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'MP', '_ormbases': ['reps.Representative']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'an_commissions': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'an_debates': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'an_id': ('django.db.models.fields.IntegerField', [], {}),
            'an_propositions': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'an_questions': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'an_reports': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'an_speeches': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'an_webpage': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'birth_department': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'circonscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps.Circonscription']", 'null': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps.Department']"}),
            'functions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mps.Function']", 'through': "orm['mps.FunctionMP']", 'symmetrical': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps.Group']"}),
            'group_role': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True'}),
            'hemicycle_sit': ('django.db.models.fields.IntegerField', [], {}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'representative_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reps.Representative']", 'unique': 'True', 'primary_key': 'True'})
        },
        'mps.phone': {
            'Meta': {'object_name': 'Phone'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps.Address']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'reps.opinion': {
            'Meta': {'object_name': 'Opinion'},
            '_author': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['reps.Representative']", 'null': 'True'}),
            '_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '400'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'reps.partyrepresentative': {
            'Meta': {'object_name': 'PartyRepresentative'},
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Party']"}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'reps.representative': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'Representative'},
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'local_party': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reps.Party']", 'through': "orm['reps.PartyRepresentative']", 'symmetrical': 'False'}),
            'opinions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reps.Opinion']", 'through': "orm['reps.OpinionREP']", 'symmetrical': 'False'}),
            'picture': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['mps']
