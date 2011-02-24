###############################################################################
# Recurse template tag for Django v1.1
# Copyright (C) 2008 Lucas Murray
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

class RecurseNode(template.Node):
    def __init__(self, var, name, child, node_list):
        template.Node.__init__(self)
        self.var = var
        self.name = name
        self.child = child
        self.node_list = node_list

    def __repr__(self):
        return '<RecurseNode>'

    def render_callback(self, context, vals, level):
        output = []
        try:
            if len(vals):
                pass
        except:
            vals = [vals]
        if len(vals):
            if 'loop' in self.node_list:
                output.append(self.node_list['loop'].render(context))
            for val in vals:
                context.push()
                context['level'] = level
                context[self.name] = val
                if 'child' in self.node_list:
                    output.append(self.node_list['child'].render(context))
                    child = self.child.resolve(context)
                    if child:
                        output.append(self.render_callback(context, child, level + 1))
                if 'endloop' in self.node_list:
                    output.append(self.node_list['endloop'].render(context))
                else:
                    output.append(self.node_list['endrecurse'].render(context))
                context.pop()
            if 'endloop' in self.node_list:
                output.append(self.node_list['endrecurse'].render(context))
        return ''.join(output)

    def render(self, context):
        vals = self.var.resolve(context)
        output = self.render_callback(context, vals, 1)
        return output

def do_recurse(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 6 and bits[2] != 'with' and bits[4] != 'as':
        msg = "Invalid tag syxtax expected '{% recurse [childVar] with [parents] as [parent] %}'"
        raise template.TemplateSyntaxError, msg
    child = parser.compile_filter(bits[1])
    var = parser.compile_filter(bits[3])
    name = bits[5]

    node_list = {}
    while len(node_list) < 4:
        temp = parser.parse(('child', 'loop', 'endloop', 'endrecurse'))
        tag = parser.tokens[0].contents
        node_list[tag] = temp
        parser.delete_first_token()
        if tag == 'endrecurse':
            break

    return RecurseNode(var, name, child, node_list)

do_recurse = register.tag('recurse', do_recurse)
