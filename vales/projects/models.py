# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from slugify import slugify

from vales.core.models import TimeStampedModel
from vales.orgs.models import Org, Membership
from vales.users.models import User


class Project(TimeStampedModel):

    title = models.CharField(
        _("Project title"),
        max_length=30,
        unique=True,
    )
    description = models.TextField(
        _('A short description of your project'),
        max_length=255,
        blank=True,
    )
    owner = models.ForeignKey(
        Membership,
        related_name='project_owner',
    )
    organization = models.ForeignKey(
        Org,
        related_name='project_org',
    )
    members = models.ManyToManyField(
        Membership,
        related_name='project_members',
    )
    slug = models.SlugField(
        max_length=30,
        blank=True,
        unique=True,
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, to_lower=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('orgs:org_detail',
                       kwargs={'slug': self.organization.slug})


    # TODO
    # tasks field (make tasks/to-do list app?)

