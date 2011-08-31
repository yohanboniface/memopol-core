from django.contrib import admin
from campaign.models import MEPScore, Campaign, ScoreRule

class ScoreRuleAdmin(admin.ModelAdmin):
    pass
admin.site.register(ScoreRule, ScoreRuleAdmin)

class MEPScoreAdmin(admin.ModelAdmin):
    pass
admin.site.register(MEPScore, MEPScoreAdmin)

class CampaignAdmin(admin.ModelAdmin):
    pass
admin.site.register(Campaign, CampaignAdmin)
