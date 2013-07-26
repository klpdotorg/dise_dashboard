from django.db import models

from common.models import BaseModel


AREA = (
    (1, 'Rural'),
    (2, 'Urban'),
)

YESNO = (
    (1, 'Yes'),
    (2, 'No')
)

SCHOOL_TYPES = (
    (1, 'Boys'),
    (2, 'Girls'),
    (3, 'Co-educational')
)

class AcademicYear(models.Model):
    from_year = models.SmallIntegerField()
    to_year = models.SmallIntegerField()

    def __unicode__(self):
        return u"%s-%s" % (self.from_year, self.to_year)


class School(BaseModel):
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
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

    def __unicode__(self):
        return u"%s (%s)" % (self.school, self.academic_year)

    class Meta:
        verbose_name_plural = 'Yearly Data'
        ordering = ('id', )


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
