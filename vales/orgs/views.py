# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging

# from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import (DetailView, ListView,
                                  UpdateView, CreateView, TemplateView)

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Org, Membership, Profile
from .forms import (OrgCreateForm, OrgUpdateForm, ProfileCreateForm,
                    ProfileUpdateForm)
from .mixins import CheckMembershipMixin, AdminRequiredMixin, ActionMixin

logger = logging.getLogger(__name__)


# Org Views
class OrgCreateView(LoginRequiredMixin, ActionMixin, CreateView):
    model = Org
    form_class = OrgCreateForm

    def form_valid(self, form):
        """
        When an Org is created, also create an instance of Membership to
        assign the Org an owner as well as adding members and users
        """
        member = Membership.objects.create(user=self.request.user)
        form.instance.owner = member
        # save the Org instance to enable post-save actions
        self.object = form.save()
        self.object.members.add(member)
        self.object.users.add(self.request.user)
        member.organization = self.object
        member.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('orgs:profile_create', kwargs={
            'slug': self.object.slug,
            'username': self.request.user.username,
        })


class OrgUpdateView(LoginRequiredMixin, ActionMixin, CheckMembershipMixin,
                    UpdateView):
    model = Org
    form_class = OrgUpdateForm
    success_msg = 'Organization updated!'
    failure_path = 'orgs:org_detail'

    def is_member(self, user, org):
        try:
            org = self.get_org()
            membership = Membership.objects.get(
                user=self.request.user,
                organization=org)
            if membership.member_profile.is_admin:
                return True
            else:
                self.success_msg = 'You need to be an Admin to update {0}.'.format(org)
                return False
        except:
            self.success_msg = 'There was an error. You need to be an Admin to update {0}.'.format(org)
            return False


class OrgListView(LoginRequiredMixin, ListView):
    model = Org

    def get_queryset(self):
        # Fetch the queryset from the parent get_queryset
        queryset = super(OrgListView, self).get_queryset()

        # Get the q GET parameter
        q = self.request.GET.get("q")
        if q:
            # Return a filtered queryset
            return queryset.filter(name__icontains=q)
        # Return the base queryset
        return queryset


class OrgDetailView(LoginRequiredMixin, DetailView):
    model = Org
    slug_field = 'slug'
    context_object_name = 'org'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(OrgDetailView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['org'] = self.object
        self.request.session['org'] = self.object.slug
        return context


# Profile Views
class ProfileCreateView(LoginRequiredMixin, ActionMixin, CheckMembershipMixin,
                        CreateView):
    model = Profile
    form_class = ProfileCreateForm
    slug_field = 'username'
    context_object_name = 'org'
    template_name_suffix = '_create_form'
    success_msg = 'Member profile created!'
    failure_path = 'orgs:org_detail'

    def get_context_data(self, **kwargs):
        context = super(ProfileCreateView, self).get_context_data(**kwargs)
        context['org'] = self.kwargs['slug']
        return context

    def is_member(self, user, org):
        try:
            org = self.get_org()
            membership = Membership.objects.get(user=user, organization=org)
            if not membership.member_profile:
                return True
            else:
                self.success_msg = 'You are already a member of {0}.'.format(org)
                return False
        except:
            return True

    def form_valid(self, form):
        """
        When a user requests to join an Org, create a Membership for the
        current user and organization to create a Profile. Then add the
        Membership to Org.members and add the User to Org.users.
        """
        org = Org.objects.get(slug=self.kwargs['slug'])

        member, created = Membership.objects.get_or_create(
            user=self.request.user,
            organization=org
        )
        form.instance.member = member
        # save the Org instance to enable post-save actions
        self.object = form.save()
        org.members.add(member)
        org.users.add(self.request.user)
        # add profile pk to session data
        self.request.session['profile_id'] = self.object.id
        return HttpResponseRedirect(self.get_success_url())
        # else:
        #     self.success_msg = 'You are already a member of {0}'.format(org)
        #     return HttpResponseRedirect(reverse(
        #         'orgs:org_detail',
        #         kwargs={'slug': org.slug})
        #     )

    def get_success_url(self):
        return reverse('orgs:profile_success', kwargs={
            'slug': self.kwargs['slug'],
            'username': self.request.user.username,
        })


class ProfileUpdateView(LoginRequiredMixin, ActionMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name_suffix = '_update_form'
    success_msg = 'Member profile updated!'

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['org'] = self.kwargs['slug']
        context['profile_id'] = self.request.session['profile_id']
        return context

    def get_success_url(self):
        return reverse('orgs:profile_detail', kwargs={
            'pk': self.object.pk,
            'slug': self.object.member.organization.slug,
            'username': self.object.member.user.username,
        })


class ProfileSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'orgs/profile_success.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileSuccessView, self).get_context_data(**kwargs)
        context['org'] = self.kwargs['slug']
        context['profile_id'] = self.request.session['profile_id']
        return context


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    context_object_name = 'profile_list'

    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
        context['org'] = Org.objects.get(slug=self.kwargs['slug'])
        return context
