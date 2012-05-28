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
    circonscription_set = fields.ToManyField("mps.api.MPCirconscriptionResource", "circonscription_set")

    class Meta:
        queryset = Department.objects.all()


class MPCirconscriptionResource(ModelResource):
    department = fields.ForeignKey(MPDepartmentResource, "department")

    class Meta:
        queryset = Circonscription.objects.all()


class MPCantonResource(ModelResource):
    circonscription = fields.ForeignKey(MPCirconscriptionResource, "circonscription")

    class Meta:
        queryset = Canton.objects.all()


class MPGroupResource(ModelResource):
    mp_set = fields.ToManyField("mps.api.MPMPResource", "mp_set")

    class Meta:
        queryset = Group.objects.all()


class MPMPResource(ModelResource):
    functionmp_set = fields.ToManyField("mps.api.MPFunctionMPResource", "functionmp_set")
    department = fields.ForeignKey(MPDepartmentResource, "department")
    group = fields.ForeignKey(MPGroupResource, "group")
    mandate_set = fields.ToManyField("mps.api.MPMandateResource", "mandate_set")
    address_set = fields.ToManyField("mps.api.MPAddressResource", "address_set")

    class Meta:
        queryset = MP.objects.all()


class MPFunctionMPResource(ModelResource):
    mp = fields.ForeignKey(MPMPResource, "mp")
    function = fields.ForeignKey(MPFunctionResource, "function")

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
