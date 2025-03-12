from django.contrib import admin
from .models import *

#
# class PromotionInline(admin.TabularInline):
#     model = Promotion
#     extra = 1
#
#
# class PersonalAdmin(admin.ModelAdmin):
#     inlines = [PromotionInline]
#
#
# admin.site.register(Personal, PersonalAdmin)
# admin.site.register(Vacancy)
admin.site.register(Personal)
admin.site.register(VisitHistory)
admin.site.register(VacationRequest)
admin.site.register(Sticker)
admin.site.register(Award)
#
