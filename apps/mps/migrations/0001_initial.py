# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Function'
        db.create_table('mps_function', (
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mps', ['Function'])

        # Adding model 'Opinion'
        db.create_table('mps_opinion', (
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1023)),
        ))
        db.send_create_signal('mps', ['Opinion'])

        # Adding model 'Department'
        db.create_table('mps_department', (
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=3, primary_key=True)),
        ))
        db.send_create_signal('mps', ['Department'])

        # Adding model 'Circonscription'
        db.create_table('mps_circonscription', (
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mps.Department'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=31)),
        ))
        db.send_create_signal('mps', ['Circonscription'])

        # Adding model 'Canton'
        db.create_table('mps_canton', (
            ('circonscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mps.Circonscription'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=511)),
        ))
        db.send_create_signal('mps', ['Canton'])

        # Adding model 'Group'
        db.create_table('mps_group', (
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=31, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mps', ['Group'])

        # Adding model 'MP'
        db.create_table('mps_mp', (
            ('an_debates', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('an_id', self.gf('django.db.models.fields.IntegerField')()),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mps.Group'])),
            ('birth_department', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('an_reports', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('profession', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('representative_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reps.Representative'], unique=True, primary_key=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mps.Department'])),
            ('an_commissions', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('an_speeches', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('an_questions', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('an_propositions', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('an_webpage', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('group_role', self.gf('django.db.models.fields.CharField')(max_length=63, null=True)),
        ))
        db.send_create_signal('mps', ['MP'])

        # Adding model 'FunctionMP'
        db.create_table('mps_functionmp', (
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mps.Function'])),
            ('mission', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mps.MP'])),
        ))
        db.send_create_signal('mps', ['FunctionMP'])

        # Adding model 'Address'
        db.create_table('mps_address', (
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=63, null=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=31)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mps.MP'])),
        ))
        db.send_create_signal('mps', ['Address'])

        # Adding model 'Phone'
        db.create_table('mps_phone', (
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mps.Address'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=63)),
        ))
        db.send_create_signal('mps', ['Phone'])

        # Adding model 'Mandate'
        db.create_table('mps_mandate', (
            ('election_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('end_term', self.gf('django.db.models.fields.DateField')(null=True)),
            ('begin_term', self.gf('django.db.models.fields.DateField')(null=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('current', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('begin_reason', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('mp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mps.MP'])),
            ('end_reason', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('mps', ['Mandate'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Function'
        db.delete_table('mps_function')

        # Deleting model 'Opinion'
        db.delete_table('mps_opinion')

        # Deleting model 'Department'
        db.delete_table('mps_department')

        # Deleting model 'Circonscription'
        db.delete_table('mps_circonscription')

        # Deleting model 'Canton'
        db.delete_table('mps_canton')

        # Deleting model 'Group'
        db.delete_table('mps_group')

        # Deleting model 'MP'
        db.delete_table('mps_mp')

        # Deleting model 'FunctionMP'
        db.delete_table('mps_functionmp')

        # Deleting model 'Address'
        db.delete_table('mps_address')

        # Deleting model 'Phone'
        db.delete_table('mps_phone')

        # Deleting model 'Mandate'
        db.delete_table('mps_mandate')
    
    
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
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
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
            'Meta': {'object_name': 'MP', '_ormbases': ['reps.Representative']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'an_commissions': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'an_debates': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'an_id': ('django.db.models.fields.IntegerField', [], {}),
            'an_propositions': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'an_questions': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'an_reports': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'an_speeches': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'an_webpage': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'birth_department': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps.Department']"}),
            'functions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mps.Function']", 'through': "orm['mps.FunctionMP']", 'symmetrical': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps.Group']"}),
            'group_role': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True'}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'representative_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reps.Representative']", 'unique': 'True', 'primary_key': 'True'})
        },
        'mps.opinion': {
            'Meta': {'object_name': 'Opinion'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1023'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
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
        }
    }
    
    complete_apps = ['mps']
