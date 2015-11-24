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


# module form
class modulesForm(forms.ModelForm):
    class Meta:
        model = modules
        fields = ('title', 'authors', 'description', 'tags')
        labels = {
            'title': 'Title (Required)',
            'authors': 'Authors (Required)',
            'description': 'Description',
            'tags': 'Tags',
        }
        widgets = {
            'title': forms.TextInput(),
            'authors': forms.TextInput(),
            'description': forms.Textarea(),
        }

class modulesRemoveForm(forms.ModelForm):
    class Meta:
        model = modules
        fields = ()


class moduleDocumentsForm(forms.ModelForm):
    class Meta:
        model = moduleDocuments
        fields = ('document', 'module', 'title', 'authors', 'description', 'tags')
        labels = {
            'document': 'File (Required)',
            'module': 'Related Module (Required)',
            'title': 'Title (Required)',
            'authors': 'Authors (Required)',
            'description': 'Description',
            'tags': 'Tags',
        }
        widgets = {
            'title': forms.TextInput(),
            'authors': forms.TextInput(),
            'description': forms.Textarea(),
        }

class moduleDocumentsRemoveForm(forms.ModelForm):
    class Meta:
        model = moduleDocuments
        fields = ()


class lectureForm(forms.ModelForm):
    class Meta:
        model = lectures
        fields = ('presentation', 'module', 'title', 'authors', 'description', 'mindate', 'maxdate', 'tags')
        labels = {
            'presentation': 'File (Required)',
            'module': 'Related Module (Required)',
            'title': 'Title (Required)',
            'authors': 'Authors (Required)',
            'description': 'Description',
            'mindate': 'Earliest Date',
            'maxdate': 'Latest Date',
            'tags': 'Tags',
        }
        widgets = {
            'title': forms.TextInput(),
            'authors': forms.TextInput(),
            'description': forms.Textarea(),
        }

class lectureRemoveForm(forms.ModelForm):
    class Meta:
        model = lectures
        fields = ()


class lecturesegmentForm(forms.ModelForm):
    class Meta:
        model = lectureSegments
        fields = ('presentation', 'lecture', 'title', 'description', 'mindate', 'maxdate', 'tags')
        labels = {
            'presentation': 'File (Required)',
            'lecture': 'Related Lecture (Required)',
            'title': 'Title (Required)',
            'description': 'Description',
            'mindate': 'Earliest Date',
            'maxdate': 'Latest Date',
            'tags': 'Tags',
        }
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
        }

class lecturesegmentRemoveForm(forms.ModelForm):
    class Meta:
        model = lectureSegments
        fields = ()


class lecturedocForm(forms.ModelForm):
    class Meta:
        model = lectureDocuments
        fields = ('document', 'lecture', 'title', 'description', 'tags')
        labels = {
            'document': 'File (Required)',
            'lecture': 'Related Lecture (Required)',
            'title': 'Title (Required)',
            'description': 'Description',
            'tags': 'Tags',
        }
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
        }

class lecturedocRemoveForm(forms.ModelForm):
    class Meta:
        model = lectureDocuments
        fields = ()


