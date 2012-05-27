from tastypie import fields
from tastypie.resources import ModelResource
from mps.models import Function,\
                       Department,\
                       Circonscription,\
                       Canton,\
                       Group,\
                       FunctionMP,\
                       Address,\
                       Phone,\
                       Mandate,\
                       MP


class MPFunctionResource(ModelResource):
    functionmp_set = fields.ToManyField("mps.api.MPFunctionMPResource", "functionmp_set")

    class Meta:
        queryset = Function.objects.all()


class MPDepartmentResource(ModelResource):
    mp_set = fields.ToManyField("mps.api.MPMPResource", "mp_set")
    class Meta:
        queryset = Department.objects.all()


class MPCirconscriptionResource(ModelResource):
    class Meta:
        queryset = Circonscription.objects.all()


class MPCantonResource(ModelResource):
    class Meta:
        queryset = Canton.objects.all()


class MPGroupResource(ModelResource):
    class Meta:
        queryset = Group.objects.all()


class MPMPResource(ModelResource):
    class Meta:
        queryset = MP.objects.all()


class MPFunctionMPResource(ModelResource):
    class Meta:
        queryset = FunctionMP.objects.all()


class MPAddressResource(ModelResource):
    class Meta:
        queryset = Address.objects.all()


class MPPhoneResource(ModelResource):
    class Meta:
        queryset = Phone.objects.all()


class MPMandateResource(ModelResource):
    class Meta:
        queryset = Mandate.objects.all()
