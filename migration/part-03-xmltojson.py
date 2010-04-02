#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys
from xml.etree import ElementTree
import codecs
import pprint

import anyjson

## Taken from activestate - Recipe 573463 (r7): Converting XML to Dictionary and back 

class XmlDictObject(dict):
    """
    Adds object like functionality to the standard dictionary.
    """

    def __init__(self, initdict=None):
        if initdict is None:
            initdict = {}
        dict.__init__(self, initdict)
    
    def __getattr__(self, item):
        return self.__getitem__(item)
    
    def __setattr__(self, item, value):
        self.__setitem__(item, value)
    
    def __str__(self):
        if self.has_key('text'):
            return self.__getitem__('text')
        else:
            return ''

    @staticmethod
    def Wrap(x):
        """
        Static method to wrap a dictionary recursively as an XmlDictObject
        """

        if isinstance(x, dict):
            return XmlDictObject((k, XmlDictObject.Wrap(v)) for (k, v) in x.iteritems())
        elif isinstance(x, list):
            return [XmlDictObject.Wrap(v) for v in x]
        else:
            return x

    @staticmethod
    def _UnWrap(x):
        if isinstance(x, dict):
            return dict((k, XmlDictObject._UnWrap(v)) for (k, v) in x.iteritems())
        elif isinstance(x, list):
            return [XmlDictObject._UnWrap(v) for v in x]
        else:
            return x
        
    def UnWrap(self):
        """
        Recursively converts an XmlDictObject to a standard dictionary and returns the result.
        """

        return XmlDictObject._UnWrap(self)


def _ConvertXmlToDictRecurse(node, dictclass):
    nodedict = dictclass()
    
    if len(node.items()) > 0:
        # if we have attributes, set them
        nodedict.update(dict(node.items()))
    
    for child in node:
        # recursively add the element's children
        newitem = _ConvertXmlToDictRecurse(child, dictclass)
        if nodedict.has_key(child.tag):
            # found duplicate tag, force a list
            if type(nodedict[child.tag]) is type([]):
                # append to existing list
                nodedict[child.tag].append(newitem)
            else:
                # convert to list
                nodedict[child.tag] = [nodedict[child.tag], newitem]
        else:
            # only one, directly set the dictionary
            nodedict[child.tag] = newitem

    if node.text is None: 
        text = ''
    else: 
        text = node.text.strip()
    
    if len(nodedict) > 0:            
        # if we have a dictionary add the text as a dictionary value (if there is any)
        if len(text) > 0:
            nodedict['text'] = text
    else:
        # if we don't have child nodes or attributes, just set the text
        nodedict = text
        
    return nodedict
        
def ConvertXmlToDict(root, dictclass=XmlDictObject):
    """
    Converts an XML file or ElementTree Element to a dictionary
    """

    # If a string is passed in, try to open it as a file
    if type(root) == type(''):
        root = ElementTree.parse(root).getroot()
    elif not isinstance(root, ElementTree._ElementInterface):
        raise TypeError, 'Expected ElementTree.Element or file path string'

    return dictclass({root.tag: _ConvertXmlToDictRecurse(root, dictclass)})


class FixupException(Exception):
    def __init__(self, message, item):
        Exception.__init__(self, message)
        self.item = item

    def __str__(self):
        return "FixupException: '%s' in [%s]" % (self.message, repr(self.item))

def fixup_gender(item):
    g = unicode(item["infos"]["birth"]["gender"])
    del item["infos"]["birth"]["gender"]
    if g == u'N\xe9':
        item["infos"]["gender"] = "M"
    elif g == u'N\xe9e':
        item["infos"]["gender"] = "F"
    else:
        item["infos"]["gender"] = "?"

def fixup_month_names(item):
    m = unicode(item["infos"]["birth"]["date"]["month"].lower())
    if len(m) == 0:
        return
    months = {
        u"janvier": "01",
        u"fevrier": "02", u"f\xe9vrier": "02",
        u"mars": "03",
        u"avril": "04",
        u"mai": "05",
        u"juin": "06",
        u"juillet": "07",
        u"aout": "08", u"ao\xfbt": "08",
        u"septembre": "09",
        u"octobre": "10",
        u"novembre": "11",
        u"decembre": "12", u"d\xe9cembre": "12",
    }
    mindex = months.get(m, None)
    if mindex is None:
        raise FixupException("Strange month [%s]" % m, item)
    item["infos"]["birth"]["date"]["month"] = mindex


def transform(item):
    try:
        item["_id"] = item["infos"]["name"]["wiki"]
        fixup_gender(item)
        fixup_month_names(item)
    except KeyError:
        pass
    except FixupException, fe:
        print fe
    return item


input_name = sys.argv[1]
output_name = sys.argv[2]

root = ElementTree.parse(input_name).getroot()

outlist = []
for pol in root.findall(root[0].tag):
    o = ConvertXmlToDict(pol)
    # we make a list of every item, skipping the toplevel tag
    item = transform(o.values()[0])
    outlist.append(item)

# now write the ugly-ass enormous list of items

outfp = codecs.open(output_name, 'wt', 'utf-8')
outfp.write(anyjson.serialize(outlist))
outfp.close()
