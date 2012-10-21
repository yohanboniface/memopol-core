# -*- coding: utf-8 -*-
__doc__ = """This module allow to run tasks on a queryset per category.
As a simple example you can have a look at :class:`WorstScore`.
"""
from categories.models import Category
from meps.models import MEP
import logging

log = logging.getLogger('crontab')


class Base(object):
    """Base task. Define hooks and a __task__ to retrieve tasks.
    subclasses must override process_entry() and may call add_category()
    """
    __task__ = True
    queryset = None
    category_slug = None

    def __init__(self):
        try:
            self.category = Category.objects.get(slug=self.category_slug)
        except Category.DoesNotExist, e:
            log.exception(e)

    def get_queryset(self):
        return self.queryset.all()

    def delete_existings(self):
        qs = self.category.representative_set.through.objects.filter(
                                                  category=self.category).all()
        try:
            qs.delete()
        except:
            # qs is to large to be delete in one step
            for obj in qs:
                obj.delete()

    def add_category(self, entry):
        entry.achievements.add(self.category)
        entry.save()

    def process_entry(self, entry):
        raise NotImplementedError()

    def __call__(self):
        log.info('Delete existing %s', self.category)
        self.delete_existings()
        log.info('Processing %s', self.category)
        for entry in self.get_queryset():
            try:
                self.process_entry(entry)
            except Exception, e:
                log.error('Error while processing %s for %s',
                          self.category, entry)
                log.exception(e)


class WorstScore(Base):
    category_slug = 'worst-score'
    queryset = MEP.objects.filter(total_score__lt=30)

    def process_entry(self, entry):
        if entry.total_score < 30:
            self.add_category(entry)
