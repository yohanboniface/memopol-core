from tastypie.resources import ModelResource
from mps.models import Function,\
                       Department,\
                       Circonscription,\
                       Canton,\
                       Group,\
                       FunctionMP,\
                       Address,\
                       Phone,\
                       Mandate


class MPFunctionResource(ModelResource):
    class Meta:
        queryset = Function.objects.all()


class MPDepartmentResource(ModelResource):
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
