# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import logging
from django.db.models import signals
from django.conf import settings
from whoosh import fields
from whoosh.support.charset import accent_map
from whoosh.support.charset import charset_table_to_dict, default_charset
from whoosh.filedb.filestore import FileStorage
from whoosh import analysis as anal


log = logging.getLogger(__name__)

class MemopolFilter(anal.Filter):

    def __call__(self, tokens):
        for t in tokens:
            if len(t.text) > 3:
                for i in range(3, 6):
                    nt = t.copy()
                    nt.text = t.text[:i]
                    yield nt
            yield t

class UniqueFilter(anal.Filter):

    def __call__(self, tokens):
        v = set()
        for t in tokens:
            if t.text not in v:
                v.add(t.text)
                yield t

def MemopolAnal():
    charmap = charset_table_to_dict(default_charset)
    return anal.RegexTokenizer(r"\w+") | anal.LowercaseFilter() | anal.CharsetFilter(accent_map)

WHOOSH_SCHEMA = fields.Schema(title=fields.TEXT(analyzer=MemopolAnal(), stored=True),
                              content=fields.TEXT(analyzer=MemopolAnal()),
                              type=fields.KEYWORD(scorable=False, stored=True),
                              url=fields.ID(stored=True, unique=True))

def create_index(sender=None, **kwargs):
    if not os.path.exists(settings.WHOOSH_INDEX):
        os.mkdir(settings.WHOOSH_INDEX)
        storage = FileStorage(settings.WHOOSH_INDEX)
        storage.create_index(WHOOSH_SCHEMA, indexname='memopol')

signals.post_syncdb.connect(create_index)

def update_index(sender, instance, created, **kwargs):
    if int(os.environ.get('SKIP_SEARCH_INDEX', '0')):
        return
    try:
        url = unicode(instance.get_absolute_url())
    except Exception:
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
                            type=unicode(instance.__class__.__name__.lower()),
                            url=url)
        writer.commit()
    else:
        writer.update_document(title=unicode(instance), content=content,
                               type=unicode(instance.__class__.__name__.lower()),
                               url=url)
        writer.commit()

class Searchables(list):
    items = []


def searchable(klass):
    if hasattr(klass, 'get_absolute_url'):
        signals.post_save.connect(update_index, sender=klass)
        Searchables.items.append(klass)
        if not hasattr(klass, 'content'):
            log.warn('%s is declared as searchable but has no content attribute' % klass)
    else:
        log.warn('%s is declared as searchable but has no get_absolute_url' % klass)
    return klass

def update():
    from meps import models
    from mps import models
    from reps import models
    import shutil
    shutil.rmtree(settings.WHOOSH_INDEX)
    create_index()
    for klass in Searchables.items:
        for i in klass.objects.all():
            update_index(None, i, created=False)

if __name__ == '__main__':
    update()
