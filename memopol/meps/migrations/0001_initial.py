# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Country'
        db.create_table('meps_country', (
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('meps', ['Country'])

        # Adding model 'Group'
        db.create_table('meps_group', (
            ('abbreviation', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('meps', ['Group'])

        # Adding model 'Delegation'
        db.create_table('meps_delegation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('meps', ['Delegation'])

        # Adding model 'Committee'
        db.create_table('meps_committee', (
            ('abbreviation', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('meps', ['Committee'])

        # Adding model 'Building'
        db.create_table('meps_building', (
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
        ))
        db.send_create_signal('meps', ['Building'])

        # Adding model 'MEP'
        db.create_table('meps_mep', (
            ('bxl_office', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ep_id', self.gf('django.db.models.fields.IntegerField')()),
            ('representative_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reps.Representative'], unique=True, primary_key=True)),
            ('stg_building', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stg_building', to=orm['meps.Building'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meps.Group'])),
            ('ep_reports', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('stg_phone1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('stg_phone2', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ep_debates', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('ep_webpage', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('stg_office', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bxl_phone2', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_role', self.gf('django.db.models.fields.CharField')(max_length=63)),
            ('ep_declarations', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('bxl_fax', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('bxl_building', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bxl_building', to=orm['meps.Building'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meps.Country'])),
            ('stg_fax', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ep_opinions', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('bxl_phone1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ep_questions', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('ep_motions', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('meps', ['MEP'])

        # Adding model 'DelegationRole'
        db.create_table('meps_delegationrole', (
            ('begin', self.gf('django.db.models.fields.DateField')(null=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mep', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meps.MEP'])),
            ('delegation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meps.Delegation'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('meps', ['DelegationRole'])

        # Adding model 'CommitteeRole'
        db.create_table('meps_committeerole', (
            ('begin', self.gf('django.db.models.fields.DateField')(null=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mep', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meps.MEP'])),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meps.Committee'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('meps', ['CommitteeRole'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table('meps_country')

        # Deleting model 'Group'
        db.delete_table('meps_group')

        # Deleting model 'Delegation'
        db.delete_table('meps_delegation')

        # Deleting model 'Committee'
        db.delete_table('meps_committee')

        # Deleting model 'Building'
        db.delete_table('meps_building')

        # Deleting model 'MEP'
        db.delete_table('meps_mep')

        # Deleting model 'DelegationRole'
        db.delete_table('meps_delegationrole')

        # Deleting model 'CommitteeRole'
        db.delete_table('meps_committeerole')
    
    
    models = {
        'meps.building': {
            'Meta': {'object_name': 'Building'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'meps.committee': {
            'Meta': {'object_name': 'Committee'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'meps.committeerole': {
            'Meta': {'object_name': 'CommitteeRole'},
            'begin': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.Committee']"}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mep': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.MEP']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'meps.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'meps.delegation': {
            'Meta': {'object_name': 'Delegation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'meps.delegationrole': {
            'Meta': {'object_name': 'DelegationRole'},
            'begin': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'delegation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.Delegation']"}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mep': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.MEP']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'meps.group': {
            'Meta': {'object_name': 'Group'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'meps.mep': {
            'Meta': {'object_name': 'MEP', '_ormbases': ['reps.Representative']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'bxl_building': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bxl_building'", 'to': "orm['meps.Building']"}),
            'bxl_fax': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bxl_office': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bxl_phone1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bxl_phone2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'committees': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meps.Committee']", 'through': "orm['meps.CommitteeRole']", 'symmetrical': 'False'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.Country']"}),
            'delegations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meps.Delegation']", 'through': "orm['meps.DelegationRole']", 'symmetrical': 'False'}),
            'ep_debates': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'ep_declarations': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'ep_id': ('django.db.models.fields.IntegerField', [], {}),
            'ep_motions': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'ep_opinions': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'ep_questions': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'ep_reports': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'ep_webpage': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.Group']"}),
            'group_role': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'representative_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reps.Representative']", 'unique': 'True', 'primary_key': 'True'}),
            'stg_building': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stg_building'", 'to': "orm['meps.Building']"}),
            'stg_fax': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'stg_office': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'stg_phone1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'stg_phone2': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
    
    complete_apps = ['meps']
