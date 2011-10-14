#encoding: utf-8
from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    title = models.CharField(max_length=100)
    site = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to='companies', null=True, blank=True)

    def __unicode__(self):
        return self.title


class Speaker(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.ForeignKey(Company)
    photo = models.ImageField(upload_to='speakers', null=True, blank=True)
    description = models.TextField(blank=True)
    site = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return u'%s %s, %s' % (self.first_name, self.last_name, self.company)


class Lecture(models.Model):
    speaker = models.ForeignKey(Speaker, null=True, blank=True)
    is_brake = models.BooleanField(default=False)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)
    is_disabled = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('start',)
    

class PartnerSection(models.Model):
    title = models.CharField(max_length=100)


class Partner(models.Model):
    section = models.ForeignKey(PartnerSection, null=True, blank=True)
    logo = models.ImageField(upload_to='partners')
    link = models.URLField(null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True)