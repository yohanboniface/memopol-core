# -*- coding: utf-8 -*-
import os
from django.core.management.base import NoArgsCommand
from optparse import make_option
from django.conf import settings

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        from meps import models
        from mps import models
        from reps import models
        from search import create_index
        from search import Searchables
        from search import update_index
        import shutil
        if os.path.isdir(settings.WHOOSH_INDEX):
            shutil.rmtree(settings.WHOOSH_INDEX)
        create_index()
        for klass in Searchables.items:
            print 'indexing %s' % klass.__name__
            for i in klass.objects.all():
                update_index(None, i, created=False)

