# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):

        if not db.dry_run:
            for i in orm.MEP.objects.all():
                if orm.MEP.objects.filter(ep_id=i.ep_id).count() > 1:
                    for die in orm.MEP.objects.filter(ep_id=i.ep_id)[1:]:
                        die.delete()
        # Adding unique constraint on 'MEP', fields ['ep_id']
        db.create_unique('meps_mep', ['ep_id'])


    def backwards(self, orm):

        # Removing unique constraint on 'MEP', fields ['ep_id']
        db.delete_unique('meps_mep', ['ep_id'])


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
        'meps.countrymep': {
            'Meta': {'object_name': 'CountryMEP'},
            'begin': ('django.db.models.fields.DateField', [], {}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.Country']"}),
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mep': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.MEP']"}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Party']"})
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
        'meps.groupmep': {
            'Meta': {'object_name': 'GroupMEP'},
            'begin': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mep': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.MEP']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'meps.mep': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'MEP', '_ormbases': ['reps.Representative']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bxl_building': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bxl_building'", 'to': "orm['meps.Building']"}),
            'bxl_fax': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bxl_office': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bxl_phone1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bxl_phone2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'committees': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meps.Committee']", 'through': "orm['meps.CommitteeRole']", 'symmetrical': 'False'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meps.Country']", 'through': "orm['meps.CountryMEP']", 'symmetrical': 'False'}),
            'delegations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meps.Delegation']", 'through': "orm['meps.DelegationRole']", 'symmetrical': 'False'}),
            'ep_debates': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'ep_declarations': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'ep_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'ep_motions': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'ep_opinions': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'ep_questions': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'ep_reports': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'ep_webpage': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meps.Group']", 'through': "orm['meps.GroupMEP']", 'symmetrical': 'False'}),
            'organizations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meps.Organization']", 'through': "orm['meps.OrganizationMEP']", 'symmetrical': 'False'}),
            'representative_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reps.Representative']", 'unique': 'True', 'primary_key': 'True'}),
            'stg_building': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stg_building'", 'to': "orm['meps.Building']"}),
            'stg_fax': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'stg_office': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'stg_phone1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'stg_phone2': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'meps.organization': {
            'Meta': {'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'meps.organizationmep': {
            'Meta': {'object_name': 'OrganizationMEP'},
            'begin': ('django.db.models.fields.DateField', [], {}),
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mep': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.MEP']"}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.Organization']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'meps.postaladdress': {
            'Meta': {'object_name': 'PostalAddress'},
            'addr': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mep': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.MEP']"})
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
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Party']"}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'reps.representative': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'Representative'},
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
