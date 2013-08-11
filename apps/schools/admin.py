from django.contrib import admin

from .models import *


class BaseTabularAdmin(admin.TabularInline):
    readonly_fields = ("date_created", "date_modified",)


class RoomTabularAdmin(BaseTabularAdmin):
    model = Room


class ToiletTabularAdmin(BaseTabularAdmin):
    model = Toilet


class EnrolmentTabularAdmin(BaseTabularAdmin):
    model = Enrolment


class YearlyDataAdmin(admin.ModelAdmin):
    raw_id_fields = ("academic_year", "school", "cluster", "village",)
    readonly_fields = ("date_created", "date_modified",)
    search_fields = ("school__name", "school__code")
    list_display = (
        "school", "academic_year", "area_type", "type"
    )
    inlines = (RoomTabularAdmin, ToiletTabularAdmin, EnrolmentTabularAdmin)
admin.site.register(YearlyData, YearlyDataAdmin)

admin.site.register([
    School,
    InstractionMedium,
    SchoolManaagement,
    SchoolCategory,
    ResidentialType,
    AcademicYear,
    SchoolBuildingStatus,
    DrinkingWaterSource,
    BoundaryWallType
])
