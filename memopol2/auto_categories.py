# -*- coding: utf-8 -*-
from categories.models import Category


class Base(object):
    __task__ = True
    queryset = None
    category_slug = None

    def __init__(self):
        self.category = Category.objects.get(slug=self.category_slug)


    def get_queryset(self):
        return self.queryset.all()

def main():


