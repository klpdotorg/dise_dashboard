from django.contrib import admin

from .models import *


class YearlyDataAdmin(admin.ModelAdmin):
    raw_id_fields = ("academic_year", "school", "cluster", "village",)
    readonly_fields = ("date_created", "date_modified",)
admin.site.register(YearlyData, YearlyDataAdmin)

admin.site.register([
    School,
    InstractionMedium,
    SchoolManaagement,
    SchoolCategory,
    ResidentialType,
    AcademicYear,
])
