# encoding: utf-8
import sys
from south.v2 import DataMigration
from django.template.defaultfilters import slugify

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."

        gender_convertion_dict = {
            u"F": 1,
            u"M": 2
        }
        total = orm["mps.mp"].objects.count()
        for number, mp in enumerate(orm["mps.mp"].objects.all(), 1):
            sys.stdout.write("mps %s/%s\r" % (number, total))
            sys.stdout.flush()
            orm["mps.MP_FR"].objects.create(
                full_name=mp.full_name if mp.full_name else mp.first_name + " " + mp.last_name,
                first_name=mp.first_name,
                last_name=mp.last_name,
                gender=gender_convertion_dict.get(mp.gender, 0),
                birth_date=mp.birth_date,
                birth_place=mp.birth_place,
                remote_id=mp.an_id,
                cv=mp.profession,
                slug=slugify(mp.full_name if mp.full_name else mp.first_name + " " + mp.last_name),
            )
        sys.stdout.write("\n")


    def backwards(self, orm):
        "Write your backwards methods here."

        orm["mps.MP_FR"].objects.all().delete()


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
        'mps.mp_fr': {
            'Meta': {'object_name': 'MP_FR', '_ormbases': ['representatives.Representative']},
            'representative_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['representatives.Representative']", 'unique': 'True', 'primary_key': 'True'})
        },
        'mps.phone': {
            'Meta': {'object_name': 'Phone'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps.Address']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5'})
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
        }
    }

    complete_apps = ['mps']
