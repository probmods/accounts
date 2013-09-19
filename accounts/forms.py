from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm
from django.utils.translation import ugettext_lazy as _

from accounts.models import PmcUser


class PmcUserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required fields, plus a
    repeated password.
    """
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
        'institution_required': _("Please enter an institution"),
        'education_status_required':_("Please select an education status"),
    }

    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))
    PROF, PSTD, PHDS, UDGD, OTHR = 'Professor', 'Post-doc', 'Ph.D Student', 'Undergrad', 'Other'    
    EDUCATION_CHOICES = ((UDGD, 'Undergrad'),
                          (PHDS, 'Ph.D Student'),
                          (PSTD, 'Post-doc'),
                          (PROF, 'Professor'),
                          (OTHR, 'Other'),
                        )
    education_status= forms.ChoiceField(choices=EDUCATION_CHOICES, widget=forms.RadioSelect)
    other = forms.CharField(max_length=100,label="If Other, enter education status:", required=False)
    
    class Meta:
        model = PmcUser
        fields = ('email','institution','name',)

    ## it doesn't seem like the Vvalidation [sic] code is actually called,
    ## which makes me think this code is redundant with the blank checking field
    ## stuff that django does
    # def clean_education(self):
    #     education_status = self.cleaned_data.get('education_status')
    #     if not education_status:
    #         forms.VvalidationError(self.error_message['education_status_required'])
    #     if education_status == 'Other':
    #         return self.cleaned_data.get('other')
    #     else:
    #         return education_status
            
    # def clean_institution(self):
    #     institution = self.cleaned_data.get('institution')
    #     if not institution:
    #         raise forms.ValidationError(self.error_message['institution_required'])
    #     return institution
        
    def clean_email(self):
        # Since EmailUser.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            PmcUser._default_manager.get(email=email)
        except PmcUser.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(PmcUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PmcUserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on the user, but
    replaces the password field with admin's password hash display field.
    """

    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = PmcUser
        fields = ('email','name', 'institution',)
        
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')
        self.fields['institution'].required = True
        self.fields['education_status'].required = True
        

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"] 
