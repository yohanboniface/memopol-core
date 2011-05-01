from models import Committe, Deleguation, Country, Group, Opinion, MEP, Party, WebSite, CommitteRole, DeleguationRole, OpinionMep
from django.contrib import admin

admin.site.register(MEP)
admin.site.register(Committe)
admin.site.register(CommitteRole)
admin.site.register(Deleguation)
admin.site.register(DeleguationRole)
admin.site.register(Country)
admin.site.register(Group)
admin.site.register(Party)
admin.site.register(Opinion)
admin.site.register(OpinionMep)
admin.site.register(WebSite)
