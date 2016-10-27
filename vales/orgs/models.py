# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from slugify import slugify

from vales.users.models import User
from vales.core.models import TimeStampedModel


class Org(TimeStampedModel):

    name = models.CharField(
        _("Your organization's name"),
        max_length=30,
        unique=True,
    )
    url = models.URLField(
        _("Your organization's Website"),
        unique=True,
        blank=True,
    )
    description = models.TextField(
        _('A short description of your organization'),
        max_length=255,
        blank=True,
    )
    owner = models.ForeignKey(
        'Membership',
        related_name='org_owner',
    )
    members = models.ManyToManyField(  # Not being assinged
        'Membership',
        related_name='org_members'
    )
    users = models.ManyToManyField(  # Not being assigned
        User,
        related_name='org_users'
    )
    slug = models.SlugField(
        max_length=30,
        blank=True,
        unique=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, to_lower=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('orgs:org_detail', kwargs={'slug': self.slug})


class Membership(TimeStampedModel):

    user = models.ForeignKey(
        User,
        related_name='memberships',
    )
    organization = models.ForeignKey(
        Org,
        related_name='member_org',
        null=True,
    )

    def __str__(self):
        return self.user.username


class Profile(TimeStampedModel):

    member = models.OneToOneField(
        Membership,
        related_name='member_profile'
    )
    department = models.CharField(
        max_length=255,
        blank=True,
    )
    position = models.CharField(
        max_length=255,
        blank=True,
    )
    is_admin = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.member.user.full_name

    def get_absolute_url(self):
        return reverse(
            'orgs:profile_detail',
            kwargs={
                'pk': self.pk,
                'username': self.member.user.username,
                'slug': self.member.organization.slug,
            }
        )
