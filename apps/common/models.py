from django.db import models
from datetime import datetime


class BaseManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return super(BaseManager, self).get_query_set().select_related()


class BaseModel(models.Model):
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()

    objects = BaseManager()

    class Meta:
        abstract = True
        ordering = ('id', )

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = datetime.now()
        self.date_modified = datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)


class Cluster(models.Model):
    name = models.CharField(max_length=255)
    block = models.ForeignKey('Block', blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.name


class Block(models.Model):
    name = models.CharField(max_length=255, unique=True)
    education_district = models.ForeignKey('EducationDistrict', blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.name


class EducationDistrict(models.Model):
    name = models.CharField(max_length=255, unique=True)
    state = models.ForeignKey('State', blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.name


class Village(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        ordering = ('name', )


class State(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u"%s" % self.name
