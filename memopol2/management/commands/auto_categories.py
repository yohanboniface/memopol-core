# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Assign auto categories'

    def handle(self, *args, **options):
        from memopol2 import auto_categories
        for name, value in auto_categories.__dict__.items():
            if hasattr(
            try:
                issubclass(value
        auto_categories.main()
