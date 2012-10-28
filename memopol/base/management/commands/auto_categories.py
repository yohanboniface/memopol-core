# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import logging

log = logging.getLogger('crontab')


class Command(BaseCommand):
    help = 'Assign auto categories'

    def handle(self, *args, **options):
        from memopol.base import auto_categories
        tasks = []
        for name, value in auto_categories.__dict__.items():
            if hasattr(value, '__task__') and not name.startswith('Base'):
                tasks.append(value)
                log.debug('Adding %s to queue', value)
        for task in tasks:
            instance = task()
            instance()
