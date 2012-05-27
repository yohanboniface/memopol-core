from tastypie import fields
from tastypie.resources import ModelResource
from meps.models import Country,\
                        LocalParty,\
                        Group,\
                        Delegation,\
                        Committee,\
                        Building,\
                        Organization,\
                        MEP,\
                        GroupMEP,\
                        DelegationRole,\
                        CommitteeRole,\
                        PostalAddress,\
                        CountryMEP,\
                        OrganizationMEP


class MEPCountryResource(ModelResource):
    class Meta:
        queryset = Country.objects.all()


class MEPLocalPartyResource(ModelResource):
    country = fields.ForeignKey(MEPCountryResource, "country")
    class Meta:
        queryset = LocalParty.objects.all()


class MEPGroupResource(ModelResource):
    class Meta:
        queryset = Group.objects.all()


class MEPDelegationResource(ModelResource):
    class Meta:
        queryset = Delegation.objects.all()


class MEPCommitteeResource(ModelResource):
    class Meta:
        queryset = Committee.objects.all()


class MEPBuildingResource(ModelResource):
    class Meta:
        queryset = Building.objects.all()


class MEPOrganizationResource(ModelResource):
    class Meta:
        queryset = Organization.objects.all()


class MEPMEPResource(ModelResource):
    bxl_building = fields.ForeignKey(MEPBuildingResource, "bxl_building")
    stg_building = fields.ForeignKey(MEPBuildingResource, "stg_building")
    class Meta:
        queryset = MEP.objects.all()


class MEPGroupMEPResource(ModelResource):
    group = fields.ForeignKey(MEPGroupResource, "group")
    mep = fields.ForeignKey(MEPMEPResource, "mep")
    class Meta:
        queryset = GroupMEP.objects.all()


class MEPDelegationRoleResource(ModelResource):
    class Meta:
        queryset = DelegationRole.objects.all()


class MEPCommitteeRoleResource(ModelResource):
    class Meta:
        queryset = CommitteeRole.objects.all()


class MEPPostalAddressResource(ModelResource):
    class Meta:
        queryset = PostalAddress.objects.all()


class MEPCountryMEPResource(ModelResource):
    class Meta:
        queryset = CountryMEP.objects.all()


class MEPOrganizationMEPResource(ModelResource):
    class Meta:
        queryset = OrganizationMEP.objects.all()
