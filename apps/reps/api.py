from tastypie import fields
from tastypie.resources import ModelResource
from reps.models import Party,\
                        Opinion,\
                        Representative,\
                        PartyRepresentative,\
                        Email,\
                        CV,\
                        WebSite,\
                        OpinionREP


class REPPartyResource(ModelResource):
    partyrepresentative_set = fields.ToManyField("reps.api.REPPartyRepresentativeResource", "partyrepresentative_set")

    class Meta:
        queryset = Party.objects.all()


class REPOpinionResource(ModelResource):
    class Meta:
        queryset = Opinion.objects.all()


class REPRepresentativeResource(ModelResource):
    class Meta:
        queryset = Representative.objects.all()


class REPPartyRepresentativeResource(ModelResource):
    class Meta:
        queryset = PartyRepresentative.objects.all()


class REPEmailResource(ModelResource):
    class Meta:
        queryset = Email.objects.all()


class REPCVResource(ModelResource):
    class Meta:
        queryset = CV.objects.all()


class REPWebSiteResource(ModelResource):
    class Meta:
        queryset = WebSite.objects.all()


class REPOpinionREPResource(ModelResource):
    class Meta:
        queryset = OpinionREP.objects.all()
