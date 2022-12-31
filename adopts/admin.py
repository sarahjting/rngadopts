from django.contrib import admin
from adopts.models import Adopt, AdoptMod


class AdoptAdmin(admin.ModelAdmin):
    model = Adopt
    list_display = ["name", "short_name", "width", "height",]


class AdoptModAdmin(admin.ModelAdmin):
    model = AdoptMod
    list_display = ["adopt", "mod",]


admin.site.register(Adopt, AdoptAdmin)
admin.site.register(AdoptMod, AdoptModAdmin)
