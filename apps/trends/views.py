from django.views.generic.simple import direct_to_template
from django.conf import settings

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot

from os.path import realpath

from meps.models import MEP

def big_mess(request):
    mep_ = MEP.view('meps/by_id', key="AlexanderAlvaro").first()
    score_list = mep_.scores
    pyplot.plot([x['value'] for x in score_list])
    print [score_list]
    pyplot.savefig(realpath("./%simg/trends/a.png" % settings.MEDIA_URL), format="png")
    context = {
        'trends' : ['a'],
    }
    return direct_to_template(request, 'trends.html', context)
