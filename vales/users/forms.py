from django import forms


class SignupForm(forms.Form):
    short_name = forms.CharField(max_length=30, label='Short name')
    full_name = forms.CharField(max_length=100, label='Full name')

    def signup(self, request, user):
        user.short_name = self.cleaned_data['short_name']
        user.full_name = self.cleaned_data['full_name']
        user.save()
