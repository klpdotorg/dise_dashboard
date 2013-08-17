from django.db import models

from common.models import BaseModel

def search_choices(t, value):
    """
    looks for index in a tuple of tuples

    >>> search_choices(YESNO, 'Yes')
    1

    """
    for k, v in t:
        if v == value:
            return k
    return False

AREA = (
    (1, 'Rural'),
    (2, 'Urban'),
)

YESNO = (
    (0, 'Not Applicable'),
    (1, 'Yes'),
    (2, 'No'),
    (3, 'Yes but not functional')
)

SCHOOL_TYPES = (
    (1, 'Boys'),
    (2, 'Girls'),
    (3, 'Co-educational')
)

ROOM_TYPES = (
    ('class', 'Classroom'),
    ('other', 'Other')
)

ROOM_CONDITIONS = (
    ('good', 'Good'),
    ('major', 'Require Major Repair'),
    ('minor', 'Require Minor Repair')
)

TOILET_TYPES = (
    ('common', 'Common'),
    ('boy', 'Boys'),
    ('girl', 'Girls')
)

class AcademicYear(models.Model):
    from_year = models.SmallIntegerField()
    to_year = models.SmallIntegerField()

    def __unicode__(self):
        return u"%s-%s" % (self.from_year, self.to_year)


class School(BaseModel):
    code = models.CharField(max_length=64, unique=True, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    pincode = models.IntegerField(blank=True, null=True)
    year_established = models.SmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        return u"%s: %s" % (self.code, self.name)


class YearlyData(BaseModel):
    academic_year = models.ForeignKey(AcademicYear)
    school = models.ForeignKey(School)

    cluster = models.ForeignKey('common.Cluster', blank=True, null=True)
    village = models.ForeignKey('common.Village', blank=True, null=True)
    ward_no = models.CharField(max_length=10, blank=True, null=True)

    management = models.ForeignKey('SchoolManaagement', blank=True, null=True)
    category = models.ForeignKey('SchoolCategory', blank=True, null=True)

    area_type = models.SmallIntegerField(choices=AREA, blank=True, null=True)
    mediums = models.ManyToManyField('InstractionMedium', blank=True, null=True)
    distance_from_brc = models.FloatField(blank=True, null=True)
    distance_from_crc = models.FloatField(blank=True, null=True)

    pre_primary_available = models.SmallIntegerField(choices=YESNO, blank=True, null=True)
    pre_primary_student_count = models.IntegerField(blank=True, null=True)
    pre_primary_teacher_count = models.IntegerField(blank=True, null=True)

    type = models.SmallIntegerField(choices=SCHOOL_TYPES, blank=True, null=True)
    part_of_shift = models.SmallIntegerField(choices=YESNO, blank=True, null=True)
    working_day_count = models.IntegerField(blank=True, null=True)

    residential = models.SmallIntegerField(choices=YESNO, blank=True, null=True)
    residential_type = models.ForeignKey('ResidentialType', blank=True, null=True)

    lowest_class = models.SmallIntegerField(blank=True, null=True)
    highest_class = models.SmallIntegerField(blank=True, null=True)

    academic_inspection_count = models.IntegerField(blank=True, null=True)
    crc_visit_count = models.IntegerField(blank=True, null=True)
    brc_visit_count = models.IntegerField(blank=True, null=True)

    development_grant_received = models.FloatField(blank=True, null=True)
    development_grant_expenditure = models.FloatField(blank=True, null=True)
    tlm_grant_received = models.FloatField(blank=True, null=True)
    tlm_grant_expenditure = models.FloatField(blank=True, null=True)
    fund_from_student_received = models.FloatField(blank=True, null=True)
    fund_from_student_expenditure = models.FloatField(blank=True, null=True)

    building_status = models.ForeignKey('SchoolBuildingStatus', blank=True, null=True)
    room_count = models.IntegerField(blank=True, null=True)
    room_for_headmaster = models.SmallIntegerField(choices=YESNO, blank=True, null=True)
    drinking_water_source = models.ForeignKey('DrinkingWaterSource', blank=True, null=True)
    electricity_status = models.SmallIntegerField(choices=YESNO, blank=True, null=True)
    boundary_wall_type = models.ForeignKey('BoundaryWallType', blank=True, null=True)

    library_available = models.SmallIntegerField(choices=YESNO, blank=True, null=True)
    library_book_count = models.IntegerField(default=0)

    playground_available = models.SmallIntegerField(choices=YESNO, blank=True, null=True)

    computer_count = models.IntegerField(default=0)
    blackboard_count = models.IntegerField(default=0)
    cal_lab_available = models.SmallIntegerField(choices=YESNO, blank=True, null=True)
    medical_checkup = models.SmallIntegerField(choices=YESNO, blank=True, null=True)
    ramp_available = models.SmallIntegerField(choices=YESNO, blank=True, null=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.school, self.academic_year)

    class Meta:
        verbose_name_plural = 'Yearly Data'
        ordering = ('id', )


class Enrolment(BaseModel):
    yearly_data = models.ForeignKey('YearlyData')
    klass = models.IntegerField(db_index=True, default=0)
    general_boys = models.IntegerField(default=0)
    general_girls = models.IntegerField(default=0)
    sc_boys = models.IntegerField(default=0)
    sc_girls = models.IntegerField(default=0)
    st_boys = models.IntegerField(default=0)
    st_girls = models.IntegerField(default=0)
    obc_boys = models.IntegerField(default=0)
    obc_girls = models.IntegerField(default=0)
    disabled_boys = models.IntegerField(default=0)
    disabled_girls = models.IntegerField(default=0)
    repeaters_boys = models.IntegerField(default=0)
    repeaters_girls = models.IntegerField(default=0)
    total_boys = models.IntegerField(db_index=True, default=0)
    total_girls = models.IntegerField(db_index=True, default=0)

    class Meta:
        unique_together = ("yearly_data", "klass")


class Room(BaseModel):
    yearly_data = models.ForeignKey('YearlyData')
    type = models.CharField(max_length=20, choices=ROOM_TYPES)
    condition = models.CharField(max_length=20, choices=ROOM_CONDITIONS)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("yearly_data", "type", "condition")


class Toilet(BaseModel):
    yearly_data = models.ForeignKey('YearlyData')
    type = models.CharField(max_length=20, choices=TOILET_TYPES)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("yearly_data", "type")


class InstractionMedium(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u"%s" % self.name


class SchoolManaagement(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name = "School Management"
        verbose_name_plural = "School Managements"


class SchoolCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'School categories'

    def __unicode__(self):
        return u"%s" % self.name


class ResidentialType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u"%s" % self.name


class SchoolBuildingStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u"%s" % self.name


class DrinkingWaterSource(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u"%s" % self.name


class BoundaryWallType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u"%s" % self.name
