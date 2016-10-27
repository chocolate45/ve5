from django import forms

from .models import Org, Profile


class OrgCreateForm(forms.ModelForm):

    class Meta:
        model = Org
        fields = ('name', 'url', 'description', )


class OrgUpdateForm(forms.ModelForm):

    class Meta:
        model = Org
        fields = ('name', 'url', 'description', )


class ProfileCreateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('department', 'position', 'is_admin', )


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('department', 'position', 'is_admin', )
