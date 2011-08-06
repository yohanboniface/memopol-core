# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import logging
from django.db.models import signals
from django.conf import settings
from whoosh import fields, index
from whoosh.filedb.filestore import FileStorage

log = logging.getLogger(__name__)

WHOOSH_SCHEMA = fields.Schema(title=fields.TEXT(stored=True),
                              content=fields.TEXT,
                              url=fields.ID(stored=True, unique=True))

def create_index(sender=None, **kwargs):
    if not os.path.exists(settings.WHOOSH_INDEX):
        os.mkdir(settings.WHOOSH_INDEX)
        storage = FileStorage(settings.WHOOSH_INDEX)
        storage.create_index(WHOOSH_SCHEMA, indexname='memopol')

signals.post_syncdb.connect(create_index)

def update_index(sender, instance, created, **kwargs):
    try:
        url = unicode(instance.get_absolute_url())
    except Exception, e:
        log.critical('Cant resolve url. Content %r not indexed' % instance)
        return

    content = getattr(instance, 'content', None)
    if content is None:
        content = unicode(instance)
    elif callable(content):
        content = content()

    storage = FileStorage(settings.WHOOSH_INDEX)
    ix = storage.open_index(indexname='memopol')
    writer = ix.writer()
    if created:
        writer.add_document(title=unicode(instance), content=content,
                            url=url)
        writer.commit()
    else:
        writer.update_document(title=unicode(instance), content=content,
                               url=url)
        writer.commit()

_searchables = []
def searchable(klass):
    if hasattr(klass, 'get_absolute_url'):
        signals.post_save.connect(update_index, sender=klass)
        _searchables.append(klass)
        if not hasattr(klass, 'content'):
            log.warn('%s is declared as searchable but has no content attribute' % klass)
    else:
        log.warn('%s is declared as searchable but has no get_absolute_url' % klass)
    return klass

def update():
    from meps import models
    from mps import models
    from reps import models
    create_index()
    for klass in _searchables:
        for i in klass.objects.all():
            update_index(None, i, created=False)

