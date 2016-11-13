from registration.forms import RegistrationForm
from django import forms
# user and profile models
from django.contrib.auth.models import User
from website.models import *

YES_NO = (
            (None, '--'),
            (True, 'Yes'),
            (False, 'No'),
        )
Null_Boolean_Choices = (
            (None, 'No Action Taken'),
            (True, 'Accepted'),
            (False, 'Rejected'),
        )

# Form for user profile model
class profileForm(RegistrationForm):
    """
        extends RegistrationForm for user profiles
    """
    name = forms.CharField(required=True, widget=forms.TextInput(), label="Full Name")
    title = forms.CharField(required=True, widget=forms.TextInput(), label="Professional Title")
    institution = forms.CharField(required=True, widget=forms.TextInput(), label="Institutional Affiliation")
    teaching = forms.CharField(required=True, widget=forms.Textarea(), label="Please describe your teaching responsibilities at your institution.")
    member = forms.BooleanField(required=False, widget=forms.Select(choices=YES_NO), label="Are you a current <a href='/membership/''>GAHTC Member</a>?")
    website = forms.URLField(required=False, widget=forms.TextInput(attrs={'placeholder': 'http://example.com/'}), label="If you are not a GAHTC Member, please provide a website link or a document that demonstrates your institutional affiliation.")
    instutution_document = forms.FileField(required=False, label="")
    introduction = forms.CharField(required=True, widget=forms.Textarea(), label="Please introduce yourself to your GAHTC colleagues.")
    avatar = forms.ImageField(required=False, label="Please upload a bio picture for others to view on the GAHTC website.")


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
        fields = ('name', 'title', 'institution', 'teaching', 'member', 'website', 'instutution_document', 'introduction', 'avatar',)
        labels = {
            'name': 'Full Name',
            'title': 'Professional Title',
            'institution': 'Institutional Affiliation',
            'teaching': 'Please describe your teaching responsibilities at your institution.',
            'member': 'Are you a current <a href="/membership/">GAHTC Member</a>?',
            'website': 'If you are not a GAHTC Member, please provide a website link or a document that demonstrates your institutional affiliation.',
            'instutution_document': '',
            'introduction': 'Please introduce yourself to your GAHTC colleagues.',
            'avatar': 'Please upload a bio picture for others to view on the GAHTC website.',
        }
        widgets = {
            'name': forms.TextInput(),
            'institution': forms.TextInput(),
            'teaching': forms.Textarea(),
            'introduction': forms.Textarea(),
            'member': forms.Select(choices=YES_NO),
            'website': forms.TextInput(attrs={'placeholder': 'http://example.com/'}),
        }

# user profile edit form
class AdminUserProfileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ('name', 'title', 'institution', 'teaching', 'member', 'website', 'instutution_document', 'introduction', 'avatar', 'verified')
        labels = {
            'name': 'Full Name',
            'title': 'Professional Title',
            'institution': 'Institutional Affiliation',
            'teaching': 'Please describe your teaching responsibilities at your institution.',
            'member': 'Are you a current <a href="/membership/">GAHTC Member</a>?',
            'website': 'If you are not a GAHTC Member, please provide a website link or a document that demonstrates your institutional affiliation.',
            'instutution_document': '',
            'introduction': 'Please introduce yourself to your GAHTC colleagues.',
            'avatar': 'Please upload a bio picture for others to view on the GAHTC website.',
            'verified': 'Please select the verification status for this user.',
        }
        widgets = {
            'name': forms.TextInput(),
            'institution': forms.TextInput(),
            'teaching': forms.Textarea(),
            'introduction': forms.Textarea(),
            'member': forms.Select(choices=YES_NO),
            'website': forms.TextInput(attrs={'placeholder': 'http://example.com/'}),
            'instutution_document': forms.ClearableFileInput(),
            'verified': forms.Select(choices=Null_Boolean_Choices),
        }

# verify users
class AdminVerifyUserForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ('verified',)
        labels = {
            'verified': 'Please select the verification status for this user.',
        }
        widgets = {
            'verified': forms.Select(choices=Null_Boolean_Choices),
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
        fields = ('lecture', 'minslidenumber', 'maxslidenumber', 'title', 'description', 'mindate', 'maxdate', 'tags')
        labels = {
            'lecture': 'Related Lecture (Required)',
            'title': 'Title (Required)',
            'minslidenumber': 'First Slide (Required)',
            'maxslidenumber': 'Last Slide (Required)',
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


# Comments Forms
class modulesCommentsForm(forms.ModelForm):    
    class Meta:
        model = modulesComments
        fields = ('comment',)
        widgets = {
            'comment': forms.widgets.Textarea(attrs={'rows': 2}),
        }

class lecturesCommentsForm(forms.ModelForm):    
    class Meta:
        model = lecturesComments
        fields = ('comment',)
        widgets = {
            'comment': forms.widgets.Textarea(attrs={'rows': 2}),
        }

class lectureSegmentsCommentsForm(forms.ModelForm):    
    class Meta:
        model = lectureSegmentsComments
        fields = ('comment',)
        widgets = {
            'comment': forms.widgets.Textarea(attrs={'rows': 2}),
        }

class lectureDocumentsCommentsForm(forms.ModelForm):    
    class Meta:
        model = lectureDocumentsComments
        fields = ('comment',)
        widgets = {
            'comment': forms.widgets.Textarea(attrs={'rows': 2}),
        }

class lectureSlidesCommentsForm(forms.ModelForm):    
    class Meta:
        model = lectureSlidesComments
        fields = ('comment',)
        widgets = {
            'comment': forms.widgets.Textarea(attrs={'rows': 2}),
        }
