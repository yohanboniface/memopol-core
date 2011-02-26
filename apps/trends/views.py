from django.views.generic.simple import direct_to_template
from django.conf import settings

from os.path import realpath

from meps.models import MEP

def big_mess(request):
    meps = MEP.view('meps/by_name')
    #positions = Position.objects.filter(mep_id=mep_id)
    for mep_ in meps:
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib import pyplot

        score_list = mep_.scores
        pyplot.plot([x['value'] for x in score_list])
        pyplot.xlabel("%s %s" % (mep_.last, mep_.first))
        print [score_list]
        pyplot.savefig(realpath("./%simg/trends/%s.png" % (settings.MEDIA_URL, mep_.id)), format="png")
        print mep_.id
        pyplot.clf()
    context = {
        'trends' : [m.id for m in meps],
    }
    return direct_to_template(request, 'trends.html', context)
