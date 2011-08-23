# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.template import Context, Template
from meps import models

meps_templates = dict(
    country=Template('''
        {% if country %}
        <a href="{% url meps:index_by_country country.code %}">
          <img src="{{ MEDIA_URL }}img/countries/small/{{ country.code }}.png"/>
          {{ country.name }}
        </a>
        {% else %}
        -
        {% endif %}
        '''),
    group=Template('''
        {% if group %}
        <a href="{% url meps:index_by_group group.abbreviation %}">
          <img class="grouplogo" src="{{ MEDIA_URL }}img/groups/eu/{{ group.abbreviation|cut:"/" }}.png" />
          {{ mep.group.abbreviation }}
        </a>
        {% else %}
        -
        {% endif %}
        '''),
    party=Template('''
    <ul class="party">
    {% for partyrepresentative in mep.partyrepresentative_set.all %}
    <li><a href="{% url meps:index_by_party partyrepresentative.party.id %}">{{ partyrepresentative.party.name }}</a></li>
    {% endfor %}
    </ul>
    '''),
)


def gen_templates():
    import settings
    dirname = os.path.dirname(__file__)
    dirname = os.path.join(dirname, 'templates', 'snippets')
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    for mep in models.MEP.objects.all():
        print mep.id
        ctx = Context(dict(mep=mep,
                           country=mep.countrymep_set.latest('end').country,
                           group=mep.groupmep_set.latest('end').group,
                           MEDIA_URL=settings.MEDIA_URL))
        for name, tmpl in meps_templates.items():
            value = tmpl.render(ctx)
            filename = os.path.join(dirname, 'mep-%s-%s.html' % (mep.id, name))
            open(filename, 'w').write(value.encode('utf-8'))
