from django.contrib.auth import get_user_model
User = get_user_model()

from django import forms
from django.utils.translation import ugettext_lazy as _

from riskgame.models import *

from email.utils import parseaddr
from passwords.fields import PasswordField

class EmailUsernameRegistrationForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"))
    password1 = PasswordField(label=_("Password"))
    password2 = PasswordField(label=_("Password (again)"))

    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        good_domains = ValidEmailDomain.objects.all().values_list('name', flat=True)
        parsed_email_domain = parseaddr(email)[1]

        if [domain for domain in good_domains if parsed_email_domain.endswith(domain)]:
            pass # Email is valid for the website
        else:
            raise forms.ValidationError(_("This e-mail address is not valid for this website."))

        if User.objects.filter(email__iexact=email):
            raise forms.ValidationError(_("This e-mail address is already in use. Please supply a different e-mail address."))

        return email

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


# class RegistrationFormTermsOfService(RegistrationForm):
#     """
#     Subclass of ``RegistrationForm`` which adds a required checkbox
#     for agreeing to a site's Terms of Service.
    
#     """
#     tos = forms.BooleanField(widget=forms.CheckboxInput,
#                              label=_(u'I have read and agree to the Terms of Service'),
#                              error_messages={'required': _("You must agree to the terms to register")})


# class RegistrationFormNoFreeEmail(RegistrationForm):
#     """
#     Subclass of ``RegistrationForm`` which disallows registration with
#     email addresses from popular free webmail services; moderately
#     useful for preventing automated spam registrations.
    
#     To change the list of banned domains, subclass this form and
#     override the attribute ``bad_domains``.
    
#     """
#     bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
#                    'googlemail.com', 'hotmail.com', 'hushmail.com',
#                    'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
#                    'yahoo.com']
    
#     def clean_email(self):
#         """
#         Check the supplied email address against a list of known free
#         webmail domains.
        
#         """
#         email_domain = self.cleaned_data['email'].split('@')[1]
#         if email_domain in self.bad_domains:
#             raise forms.ValidationError(_("Registration using free email addresses is prohibited. Please supply a different email address."))
#         return self.cleaned_data['email']
