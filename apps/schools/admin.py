from django.contrib import admin

from .models import *


class YearlyDataAdmin(admin.ModelAdmin):
    raw_id_fields = ("academic_year", "school", "cluster", "village",)
    readonly_fields = ("date_created", "date_modified",)
    search_fields = ("school__name", )
    list_display = (
        "school", "academic_year", "area_type", "type"
    )
admin.site.register(YearlyData, YearlyDataAdmin)

admin.site.register([
    School,
    InstractionMedium,
    SchoolManaagement,
    SchoolCategory,
    ResidentialType,
    AcademicYear,
])
