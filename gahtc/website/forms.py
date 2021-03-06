from registration.forms import RegistrationForm
from django import forms

# user and profile models
from django.contrib.auth.models import User
from website.models import *

# using the filter select multiple admin widget for author names
from django.contrib.admin.widgets import FilteredSelectMultiple

YES_NO = (
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
    first_name = forms.CharField(required=True, widget=forms.TextInput(), label="First Name")
    last_name = forms.CharField(required=True, widget=forms.TextInput(), label="Last Name")
    title = forms.CharField(required=True, widget=forms.TextInput(), label="Title/Academic Rank", help_text="(ex: Assistant Professor, Lecturer, Post-Doc)")
    institution = forms.CharField(required=True, widget=forms.TextInput(), label="Institutional Affiliation")
    institution_address = forms.CharField(required=True, widget=forms.TextInput(), label="Institution's Street Address")
    institution_city = forms.CharField(required=True, widget=forms.TextInput(), label="City")
    institution_country = forms.CharField(required=True, widget=forms.TextInput(), label="Country")
    institution_postal_code = forms.CharField(required=True, widget=forms.TextInput(), label="Postal Code")
    introduction = forms.CharField(required=True, widget=forms.Textarea(), label="Please provide a brief bio", help_text="(written in third person, describing your professional experience and teaching responsibilities at your current institution)")
    website = forms.URLField(required=False, widget=forms.TextInput(attrs={'placeholder': 'http://example.com/'}), label="Please provide a URL for a website that demonstrates your institutional affiliation")
    avatar = forms.ImageField(required=True, label="Please upload a profile picture")


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
        fields = ('first_name', 'last_name', 'title', 'institution', 'institution_address', 'institution_city', 'institution_country', 'institution_postal_code', 'introduction', 'website', 'avatar',)
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'title': 'Title/Academic Rank',
            'institution': 'Institutional Affiliation',
            'institution_address': 'Institution\'s Street Address',
            'institution_city': 'City',
            'institution_country': 'Country',
            'institution_postal_code': 'Postal Code',
            'website': 'Please provide a URL for a website that demonstrates your institutional affiliation',
            'introduction': 'Please provide a brief bio',
            'avatar': 'Please upload a profile picture',
        }
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'institution': forms.TextInput(),
            'institution_address': forms.TextInput(),
            'institution_city': forms.TextInput(),
            'institution_country': forms.TextInput(),
            'institution_postal_code': forms.TextInput(),
            'introduction': forms.Textarea(),
            'website': forms.TextInput(attrs={'placeholder': 'http://example.com/'}),
        }
        help_texts = {
            'title': '(ex: Assistant Professor, Lecturer, Post-Doc)',
            'introduction': '(written in third person, describing your professional experience and teaching responsibilities at your current institution)',
        }

# user profile edit form
class AdminUserProfileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ('first_name', 'last_name', 'title', 'institution', 'institution_address', 'institution_city', 'institution_country', 'institution_postal_code', 'introduction', 'website', 'avatar', 'verified', 'public')
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'title': 'Title/Academic Rank',
            'institution': 'Institutional Affiliation',
            'institution_address': 'Institution\'s Street Address',
            'institution_city': 'City',
            'institution_country': 'Country',
            'institution_postal_code': 'Postal Code',
            'website': 'Please provide a URL for a website that demonstrates your institutional affiliation',
            'introduction': 'Please provide a brief bio',
            'avatar': 'Please upload a profile picture',
            'verified': 'Please select the verification status for this user.',
            'public': 'Should this user have a public profile?',
        }
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'institution': forms.TextInput(),
            'institution_address': forms.TextInput(),
            'institution_city': forms.TextInput(),
            'institution_country': forms.TextInput(),
            'institution_postal_code': forms.TextInput(),
            'introduction': forms.Textarea(),
            'website': forms.TextInput(attrs={'placeholder': 'http://example.com/'}),
            'instutution_document': forms.ClearableFileInput(),
            'verified': forms.Select(choices=Null_Boolean_Choices),
            'public': forms.Select(choices=YES_NO),
        }
        help_texts = {
            'title': '(ex: Assistant Professor, Lecturer, Post-Doc)',
            'introduction': '(written in third person, describing your professional experience and teaching responsibilities at your current institution)',
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
        fields = ('title', 'authors_m2m', 'description', 'cover_image', 'featured', 'keywords')
        labels = {
            'title': 'Title (Required)',
            'authors_m2m': 'Authors (Required)',
            'description': 'Description',
            'cover_image': 'Cover Image',
            'featured': 'Is this a featured module?',
            'keywords': 'Keywords',
        }
        widgets = {
            'title': forms.TextInput(),
            'authors_m2m': FilteredSelectMultiple("authors", is_stacked=False),
            'description': forms.Textarea(),
            'featured': forms.Select(choices=YES_NO),
        }

class modulesRemoveForm(forms.ModelForm):
    class Meta:
        model = modules
        fields = ()


class moduleDocumentsForm(forms.ModelForm):
    class Meta:
        model = moduleDocuments
        fields = ('document', 'module', 'doc_type', 'title', 'description', 'keywords')
        labels = {
            'document': 'File (Required)',
            'module': 'Related Module (Required)',
            'doc_type': 'Document Type',
            'title': 'Title (Required)',
            'description': 'Description',
            'keywords': 'Keywords',
        }
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
        }

class moduleDocumentsRemoveForm(forms.ModelForm):
    class Meta:
        model = moduleDocuments
        fields = ()


class lectureForm(forms.ModelForm):
    class Meta:
        model = lectures
        fields = ('presentation', 'module', 'title', 'authors_m2m', 'description', 'keywords')
        labels = {
            'presentation': 'File (Required)',
            'module': 'Related Module (Required)',
            'title': 'Title (Required)',
            'authors_m2m': 'Authors (Required)',
            'description': 'Description',
            'keywords': 'Keywords',
        }
        widgets = {
            'title': forms.TextInput(),
            'authors_m2m': FilteredSelectMultiple("authors", is_stacked=False),
            'description': forms.Textarea(),
        }
        queryset = {
            'authors_m2m': profile.objects.filter(verified=True).exclude(last_name='', first_name='').order_by('last_name', 'first_name'),
        }


class lectureRemoveForm(forms.ModelForm):
    class Meta:
        model = lectures
        fields = ()


class lecturesegmentForm(forms.ModelForm):
    class Meta:
        model = lectureSegments
        fields = ('lecture', 'minslidenumber', 'maxslidenumber', 'title', 'description', 'keywords')
        labels = {
            'lecture': 'Related Lecture (Required)',
            'title': 'Title (Required)',
            'minslidenumber': 'First Slide (Required)',
            'maxslidenumber': 'Last Slide (Required)',
            'description': 'Description',
            'keywords': 'Keywords',
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
        fields = ('document', 'lecture', 'doc_type', 'title', 'description', 'keywords')
        labels = {
            'document': 'File (Required)',
            'lecture': 'Related Lecture (Required)',
            'doc_type': 'Document Type',
            'title': 'Title (Required)',
            'description': 'Description',
            'keywords': 'Keywords',
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
        labels = {
            'comment': 'member comments:',
        }
        widgets = {
            'comment': forms.widgets.Textarea(attrs={'rows': 2}),
        }

class lecturesCommentsForm(forms.ModelForm):    
    class Meta:
        model = lecturesComments
        fields = ('comment',)
        labels = {
            'comment': 'member comments:',
        }
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


# module form
class CSmodulesForm(forms.ModelForm):
    class Meta:
        model = comingSoonModules
        fields = ('title', 'authors_m2m', 'description', 'cover_image', 'keywords')
        labels = {
            'title': 'Title (Required)',
            'authors_m2m': 'Authors (Required)',
            'description': 'Description',
            'cover_image': 'Cover Image',
            'keywords': 'Keywords',
        }
        widgets = {
            'title': forms.TextInput(),
            'authors_m2m': FilteredSelectMultiple("authors", is_stacked=False),
            'description': forms.Textarea(),
        }
        queryset = {
            'authors_m2m': profile.objects.filter(verified=True).exclude(last_name='', first_name='').order_by('last_name', 'first_name'),
        }

class CSmodulesRemoveForm(forms.ModelForm):
    class Meta:
        model = comingSoonModules
        fields = ()


class docTypeAddForm(forms.ModelForm):
    class Meta:
        model = docType
        fields = ('name',)



