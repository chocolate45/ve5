# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Org


class CheckMembershipMixin(object):
    failure_path = ''  # should be namespace
    org = None

    def get_org(self):
        org = Org.objects.get(slug=self.kwargs['slug'])
        return org

    def is_member(self, user, org):
        return True

    def member_check_failed(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse(
            self.failure_path,
            kwargs={'slug': self.kwargs['slug']}
        ))

    def dispatch(self, request, *args, **kwargs):
        if not self.is_member(user=self.request.user, org=self.org):
            return self.member_check_failed(request, *args, **kwargs)
        return super(CheckMembershipMixin, self).dispatch(request, *args, **kwargs)


class AdminRequiredMixin(CheckMembershipMixin):

    def is_admin(self, user, org):
        return True


class ActionMixin(object):

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super().form_valid(form)

    def member_check_failed(self, request, *args, **kwargs):
        messages.info(self.request, self.success_msg)
        return super().member_check_failed(request, *args, **kwargs)
