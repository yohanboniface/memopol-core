from reps.models import WebSite, Party, Opinion, OpinionREP
from models import Committee, Deleguation, Country, Group, MEP, CommitteeRole, DeleguationRole
from django.contrib import admin

admin.site.register(MEP)
admin.site.register(Committee)
admin.site.register(CommitteeRole)
admin.site.register(Deleguation)
admin.site.register(DeleguationRole)
admin.site.register(Country)
admin.site.register(Group)
admin.site.register(Party)
admin.site.register(Opinion)
admin.site.register(OpinionREP)
admin.site.register(WebSite)
