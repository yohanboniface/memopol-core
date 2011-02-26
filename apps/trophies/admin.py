from django.contrib import admin
from trophies.models import ManualTrophy, AutoTrophy, Reward

admin.site.register(ManualTrophy)
admin.site.register(AutoTrophy)
admin.site.register(Reward)
