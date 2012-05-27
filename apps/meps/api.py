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
    countrymep_set = fields.ToManyField("meps.api.MEPCountryMEPResource", "countrymep_set")

    class Meta:
        queryset = Country.objects.all()


class MEPLocalPartyResource(ModelResource):
    countrymep_set = fields.ToManyField("meps.api.MEPCountryMEPResource", "countrymep_set")
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
    mep = fields.ForeignKey(MEPMEPResource, "mep")
    delegation = fields.ForeignKey(MEPDelegationResource, "delegation")

    class Meta:
        queryset = DelegationRole.objects.all()


class MEPCommitteeRoleResource(ModelResource):
    mep = fields.ForeignKey(MEPMEPResource, "mep")
    committee = fields.ForeignKey(MEPCommitteeResource, "committee")

    class Meta:
        queryset = CommitteeRole.objects.all()


class MEPPostalAddressResource(ModelResource):
    mep = fields.ForeignKey(MEPMEPResource, "mep")

    class Meta:
        queryset = PostalAddress.objects.all()


class MEPCountryMEPResource(ModelResource):
    mep = fields.ForeignKey(MEPMEPResource, "mep")
    country = fields.ForeignKey(MEPCountryResource, "country")
    party = fields.ForeignKey(MEPLocalPartyResource, "party")

    class Meta:
        queryset = CountryMEP.objects.all()


class MEPOrganizationMEPResource(ModelResource):
    mep = fields.ForeignKey(MEPMEPResource, "mep")
    organization = fields.ForeignKey(MEPOrganizationResource, "organization")

    class Meta:
        queryset = OrganizationMEP.objects.all()
