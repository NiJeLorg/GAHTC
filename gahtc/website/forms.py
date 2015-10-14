from registration.forms import RegistrationForm
from django import forms
# user and profile models
from django.contrib.auth.models import User
from website.models import *

# Form for user profile model
class profileForm(RegistrationForm):
    """
        extends RegistrationForm for user profiles
    """
    name = forms.CharField(required=True, widget=forms.TextInput(), label="Full Name")
    institution = forms.CharField(required=True, widget=forms.TextInput(), label="Institutional Affiliation")
    teaching = forms.CharField(required=True, widget=forms.Textarea(), label="Please describe your teaching responsibilities at your institution.")
    introduction = forms.CharField(required=True, widget=forms.Textarea(), label="Please introduce yourself to your GAHTC colleagues.")
    pic = forms.ImageField(required=False, label="Please upload a bio picture for others to view on the GAHTC website.")


# allow users to edit their email address in the profile form
class UserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('email',)
        
# user profile edit form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ('name', 'institution', 'teaching', 'introduction', 'pic')
        labels = {
            'name': 'Full Name',
            'institution': 'Institutional Affiliation',
            'teaching': 'Please describe your teaching responsibilities at your institution.',
            'introduction': 'Please introduce yourself to your GAHTC colleagues.',
            'pic': 'Please upload a bio picture for others to view on the GAHTC website.',
        }
        widgets = {
            'name': forms.TextInput(),
            'institution': forms.TextInput(),
            'teaching': forms.Textarea(),
            'introduction': forms.Textarea(),
        }
