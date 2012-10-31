# encoding: utf-8
import sys
from south.db import db
from south.v2 import DataMigration

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."

        total = orm["meps.committeerole"].objects.count()
        for number, committee in enumerate(orm["meps.committeerole"].objects.all(), 1):
            sys.stdout.write("committees %s/%s\r" % (number, total))
            sys.stdout.flush()
            orm["representatives.mandate"].objects.create(
                name=committee.committee.name,
                kind="committee",
                constituency="European Parliament",
                role=committee.role,
                begin_date=committee.begin,
                end_date=committee.end,
                active=True,
                short_id=committee.committee.abbreviation,
                representative=orm["representatives.representative"].objects.get(remote_id=committee.mep.ep_id),
            )
        sys.stdout.write("\n")

        total = orm["meps.delegationrole"].objects.count()
        for number, delegation in enumerate(orm["meps.delegationrole"].objects.all(), 1):
            sys.stdout.write("delegations %s/%s\r" % (number, total))
            sys.stdout.flush()
            orm["representatives.mandate"].objects.create(
                name=delegation.delegation.name,
                kind="delegation",
                constituency="European Parliament",
                role=delegation.role,
                begin_date=delegation.begin,
                end_date=delegation.end,
                active=True,
                representative=orm["representatives.representative"].objects.get(remote_id=delegation.mep.ep_id),
            )
        sys.stdout.write("\n")

        total = orm["meps.groupmep"].objects.count()
        for number, group in enumerate(orm["meps.groupmep"].objects.all(), 1):
            sys.stdout.write("groups %s/%s\r" % (number, total))
            sys.stdout.flush()
            orm["representatives.mandate"].objects.create(
                name=group.group.name,
                kind="group",
                constituency="European Parliament",
                role=group.role,
                begin_date=group.begin,
                end_date=group.end,
                active=True,
                short_id=group.group.abbreviation,
                representative=orm["representatives.representative"].objects.get(remote_id=group.mep.ep_id),
            )
        sys.stdout.write("\n")

        total = orm["meps.organizationmep"].objects.count()
        for number, organization in enumerate(orm["meps.organizationmep"].objects.all(), 1):
            sys.stdout.write("organizations %s/%s\r" % (number, total))
            sys.stdout.flush()
            orm["representatives.mandate"].objects.create(
                name=organization.organization.name,
                kind="organization",
                constituency="European Parliament",
                role=organization.role,
                begin_date=organization.begin,
                end_date=organization.end,
                active=True,
                representative=orm["representatives.representative"].objects.get(remote_id=organization.mep.ep_id),
            )
        sys.stdout.write("\n")

        total = orm["meps.countrymep"].objects.count()
        for number, country in enumerate(orm["meps.countrymep"].objects.all(), 1):
            sys.stdout.write("countries %s/%s\r" % (number, total))
            sys.stdout.flush()
            orm["representatives.mandate"].objects.create(
                name=country.country.name,
                kind="country",
                constituency=country.party.name,
                begin_date=country.begin,
                end_date=country.end,
                active=True,
                short_id=country.country.code,
                representative=orm["representatives.representative"].objects.get(remote_id=country.mep.ep_id),
            )
        sys.stdout.write("\n")

    def backwards(self, orm):
        "Write your backwards methods here."

        db.execute("DELETE FROM representatives_mandate")


    models = {
        'categories.category': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'alternate_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'alternate_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_extra': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['categories.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'thumbnail': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'thumbnail_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
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
            'Meta': {'ordering': "['code']", 'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'meps.countrymep': {
            'Meta': {'object_name': 'CountryMEP'},
            'begin': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.Country']"}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mep': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.MEP']"}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.LocalParty']"})
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
        'meps.localparty': {
            'Meta': {'object_name': 'LocalParty', '_ormbases': ['reps.Party']},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meps.Country']", 'null': 'True'}),
            'party_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reps.Party']", 'unique': 'True', 'primary_key': 'True'})
        },
        'meps.mep': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'MEP', '_ormbases': ['reps.Representative']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bxl_building': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bxl_building'", 'null': 'True', 'to': "orm['meps.Building']"}),
            'bxl_fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'bxl_floor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'bxl_office_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'bxl_phone1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'bxl_phone2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
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
            'position': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'representative_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reps.Representative']", 'unique': 'True', 'primary_key': 'True'}),
            'stg_building': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stg_building'", 'null': 'True', 'to': "orm['meps.Building']"}),
            'stg_fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'stg_floor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'stg_office_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'stg_phone1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'stg_phone2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'total_score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'})
        },
        'meps.mp_eu': {
            'Meta': {'object_name': 'MP_EU', '_ormbases': ['representatives.Representative']},
            'representative_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['representatives.Representative']", 'unique': 'True', 'primary_key': 'True'})
        },
        'meps.organization': {
            'Meta': {'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'meps.organizationmep': {
            'Meta': {'object_name': 'OrganizationMEP'},
            'begin': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
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
        'representatives.representative': {
            'Meta': {'object_name': 'Representative'},
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gender': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'representatives.mandate': {
            'Meta': {'object_name': 'Mandate'},
            'active': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'constituency': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['representatives.Representative']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'short_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
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
            'achievements': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['categories.Category']", 'symmetrical': 'False'}),
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
        },
        'reps.cv': {
            'Meta': {'object_name': 'CV'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"}),
            'title': ('django.db.models.fields.TextField', [], {}) 
        },
    }

    complete_apps = ['meps']
