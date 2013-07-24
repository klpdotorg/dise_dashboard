from django.db import models
from datetime import datetime


# class BaseModel(model.Model):
#     date_created = models.DateTimeField(default=datetime.now)

#     class Meta:
#         abstract = True


class Cluster(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u"%s" % self.name


class Block(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u"%s" % self.name


class EducationDistrict(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u"%s" % self.name


class Village(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u"%s" % self.name


class State(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u"%s" % self.name
