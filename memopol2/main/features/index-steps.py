import sys
from lettuce import *
from django.test.client import Client
from nose.tools import assert_equals

import lxml.html
from lxml.cssselect import CSSSelector

def debug(w):
    sys.stdout.flush()
    sys.stdout.write("\n-----\n")
    sys.stdout.write(w.encode("utf-8"))
    sys.stdout.write("\n-----\n")
    sys.stdout.flush()

@before.all
def set_browser():
    world.browser = Client()

@step(r'I access the url "(.*)"')
def access_url(step, url):
    response = world.browser.get(url, follow=True)
    world.dom = lxml.html.fromstring(unicode(response.content, "utf-8"))

@step(r'I see the header "(.*)"')
def see_header(step, text):
    sel = CSSSelector('h1')
    for i in sel(world.dom):
        if i.text == text:
            return
    assert False
