# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Party'
        db.create_table('reps_party', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('reps', ['Party'])

        # Adding model 'Opinion'
        db.create_table('reps_opinion', (
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1023)),
        ))
        db.send_create_signal('reps', ['Opinion'])

        # Adding model 'Representative'
        db.create_table('reps_representative', (
            ('picture', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('birth_place', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
        ))
        db.send_create_signal('reps', ['Representative'])

        # Adding model 'PartyRepresentative'
        db.create_table('reps_partyrepresentative', (
            ('current', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.Party'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.Representative'])),
        ))
        db.send_create_signal('reps', ['PartyRepresentative'])

        # Adding model 'Email'
        db.create_table('reps_email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.Representative'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('reps', ['Email'])

        # Adding model 'CV'
        db.create_table('reps_cv', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.Representative'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1023)),
        ))
        db.send_create_signal('reps', ['CV'])

        # Adding model 'WebSite'
        db.create_table('reps_website', (
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.Representative'])),
        ))
        db.send_create_signal('reps', ['WebSite'])

        # Adding model 'OpinionREP'
        db.create_table('reps_opinionrep', (
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('opinion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.Opinion'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.Representative'])),
        ))
        db.send_create_signal('reps', ['OpinionREP'])


    def backwards(self, orm):

        # Deleting model 'Party'
        db.delete_table('reps_party')

        # Deleting model 'Opinion'
        db.delete_table('reps_opinion')

        # Deleting model 'Representative'
        db.delete_table('reps_representative')

        # Deleting model 'PartyRepresentative'
        db.delete_table('reps_partyrepresentative')

        # Deleting model 'Email'
        db.delete_table('reps_email')

        # Deleting model 'CV'
        db.delete_table('reps_cv')

        # Deleting model 'WebSite'
        db.delete_table('reps_website')

        # Deleting model 'OpinionREP'
        db.delete_table('reps_opinionrep')


    models = {
        'reps.cv': {
            'Meta': {'object_name': 'CV'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1023'})
        },
        'reps.email': {
            'Meta': {'object_name': 'Email'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"})
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
        },
        'reps.website': {
            'Meta': {'object_name': 'WebSite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['reps']
