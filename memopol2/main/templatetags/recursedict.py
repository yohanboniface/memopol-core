###############################################################################
# Recurse dictionary template tag for Django v1.1
# Copyright (C) 2008 Lucas Murray, (C) 2010 Stefan Praszalowicz
# http://www.undefinedfire.com 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
###############################################################################

from django import template

register = template.Library()

class RecurseDictNode(template.Node):
    def __init__(self, var, node_list):
        template.Node.__init__(self)
        self.var = var
        self.node_list = node_list

    def __repr__(self):
        return '<RecurseDictNode>'

    def render_callback(self, context, vals, level):
        if len(vals) == 0:
            return ''

        output = []

        if 'loop' in self.node_list:
            output.append(self.node_list['loop'].render(context))

        for k, v in vals:
            context.push()
            
            context['level'] = level
            context['key'] = k
            
            if 'value' in self.node_list:
                output.append(self.node_list['value'].render(context))
                
                if type(v) == list or type(v) == tuple:
                    child_items = [ (None, x) for x in v ]
                    output.append(self.render_callback(context, child_items, level + 1))
                else:
                    try:
                        child_items = v.items()
                        output.append(self.render_callback(context, child_items, level + 1))
                    except:
                        output.append(unicode(v))
            
            if 'endloop' in self.node_list:
                output.append(self.node_list['endloop'].render(context))
            else:
                output.append(self.node_list['endrecursedict'].render(context))
            
            context.pop()

        if 'endloop' in self.node_list:
            output.append(self.node_list['endrecursedict'].render(context))

        return ''.join(output)

    def render(self, context):
        vals = self.var.resolve(context).items()
        output = self.render_callback(context, vals, 1)
        return output

def recursedict_tag(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 2 and bits[0] != 'recursedict':
        raise template.TemplateSyntaxError, "Invalid tag syxtax expected '{% recursedict [dictVar] %}'"

    var = parser.compile_filter(bits[1])
    node_list = {}
    while len(node_list) < 4:
        temp = parser.parse(('value', 'loop', 'endloop', 'endrecursedict'))
        tag = parser.tokens[0].contents
        node_list[tag] = temp
        parser.delete_first_token()
        if tag == 'endrecursedict':
            break

    return RecurseDictNode(var, node_list)

recursedict_tag = register.tag('recursedict', recursedict_tag)
