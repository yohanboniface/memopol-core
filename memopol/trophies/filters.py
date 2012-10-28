def condition_president_of_group(mep):
    """
    President of group.
    """
    return mep.infos.group.role in [u'Pr\u00e9sident', u'Copr\u00e9sident']

def condition_vp_of_group(mep):
    """
    VP of group.
    """
    return u'Vice-Pr\u00e9sident' == mep.infos.group.role

def condition_president_of_ep(mep):
    """
    President of EP.
    """
    return (u'Parlement europ\u00e9en',u'Pr\u00e9sident') in [(fn.label,fn.role) for fn in mep.functions]

def condition_vp_of_ep(mep):
    """
    VP of EP.
    """
    return ((u'Parlement europ\u00e9en',u'Vice-Pr\u00e9sident') in [(fn.label,fn.role) for fn in mep.functions])

def condition_commitee_member(mep):
    """
    Commitee member.
    """
    return [fn.role for fn in mep.functions if fn.get('abbreviation') and fn.role==u'Membre']

def condition_commitee_supplement(mep):
    """
    Commitee supplement.
    """
    return [fn.abbreviation for fn in mep.functions if fn.get('abbreviation') and fn.role==u'Membre suppl\u00e9ant']
