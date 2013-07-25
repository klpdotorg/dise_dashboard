from django.db import models

from common.models import BaseModel


class School(BaseModel):
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    pincode = models.IntegerField(blank=True, null=True)

    cluster = models.ForeignKey('common.Cluster', blank=True, null=True)
    village = models.ForeignKey('common.Village', blank=True, null=True)
    ward_no = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return u"%s: %s" % (self.code, self.name)


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
