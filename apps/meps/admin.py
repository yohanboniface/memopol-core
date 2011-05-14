from models import Committee, Deleguation, Country, Group, Opinion, MEP, Party, WebSite, CommitteRole, DeleguationRole, OpinionMEP
from django.contrib import admin

admin.site.register(MEP)
admin.site.register(Committee)
admin.site.register(CommitteRole)
admin.site.register(Deleguation)
admin.site.register(DeleguationRole)
admin.site.register(Country)
admin.site.register(Group)
admin.site.register(Party)
admin.site.register(Opinion)
admin.site.register(OpinionMEP)
admin.site.register(WebSite)
