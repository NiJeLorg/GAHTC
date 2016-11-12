from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import ugettext_lazy as _
from pybb import defaults, util
from pybb.compat import get_image_field_class, get_username_field

# import User model
from django.contrib.auth.models import User

# django taggit import
from taggit_autosuggest.managers import TaggableManager

# import ApproximateDateField
from django_date_extensions.fields import ApproximateDateField


TZ_CHOICES = [(float(x[0]), x[1]) for x in (
	(-12, '-12'), (-11, '-11'), (-10, '-10'), (-9.5, '-09.5'), (-9, '-09'),
	(-8.5, '-08.5'), (-8, '-08 PST'), (-7, '-07 MST'), (-6, '-06 CST'),
	(-5, '-05 EST'), (-4, '-04 AST'), (-3.5, '-03.5'), (-3, '-03 ADT'),
	(-2, '-02'), (-1, '-01'), (0, '00 GMT'), (1, '+01 CET'), (2, '+02'),
	(3, '+03'), (3.5, '+03.5'), (4, '+04'), (4.5, '+04.5'), (5, '+05'),
	(5.5, '+05.5'), (6, '+06'), (6.5, '+06.5'), (7, '+07'), (8, '+08'),
	(9, '+09'), (9.5, '+09.5'), (10, '+10'), (10.5, '+10.5'), (11, '+11'),
	(11.5, '+11.5'), (12, '+12'), (13, '+13'), (14, '+14'),
)]

# user profile
class profile(models.Model):

	user = models.OneToOneField(User, related_name='userProfile')
	name = models.CharField(max_length=255, default='', null=False, blank=False)
	institution = models.CharField(max_length=255, default='', null=False, blank=False)
	teaching = models.TextField(default='', null=False, blank=False)
	introduction = models.TextField(default='', null=False, blank=False)
	avatar = models.ImageField(upload_to="bio_pics/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	member = models.BooleanField(blank=True, default=False)
	website = models.URLField(max_length=255, default='', null=True, blank=True)
	instutution_document = models.FileField(upload_to="insitution_docs/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	verified = models.NullBooleanField(default=None)
	language = models.CharField(max_length=255, default='', null=True, blank=True)
	signature = models.TextField(_('Signature'), blank=True, max_length=255)
	signature_html = models.TextField(_('Signature HTML Version'), blank=True, max_length=255)
	time_zone = models.FloatField(_('Time zone'), choices=TZ_CHOICES, default=float(defaults.PYBB_DEFAULT_TIME_ZONE))
	show_signatures = models.BooleanField(_('Show signatures'), blank=True, default=True)
	post_count = models.IntegerField(_('Post count'), blank=True, default=0)
	autosubscribe = models.BooleanField(_('Automatically subscribe'), help_text=_('Automatically subscribe to topics that you answer'), default=True)

	def __unicode__(self):
		return self.name

	def get_display_name(self):
		try:
			if hasattr(self, 'user'):  # we have OneToOne foreign key to user model
				return self.user.get_username()
			if not defaults.PYBB_PROFILE_RELATED_NAME:  # we now in user custom model itself
				return self.get_username()
		except Exception:
			return unicode(self)


# course modules
class modules(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	authors = models.CharField(max_length=255, default='', null=False, blank=False)
	description = models.TextField(default='', null=True, blank=True)
	tags = TaggableManager(blank=True)

	def __unicode__(self):
		return self.title

#module documents
class moduleDocuments(models.Model):
	module = models.ForeignKey(modules, related_name='moduleDocsModule')
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	authors = models.CharField(max_length=255, default='', null=False, blank=False)
	description = models.TextField(default='', null=True, blank=True)
	document = models.FileField(upload_to="module_docs/%Y_%m_%d_%h_%M_%s", default='', null=False, blank=False)
	document_contents = models.TextField(default='', null=True, blank=True)
	extracted = models.BooleanField(default=False)
	tags = TaggableManager(blank=True)

# lectures
class lectures(models.Model):
	module = models.ForeignKey(modules, related_name='lecturesModule')
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	authors = models.CharField(max_length=255, default='', null=False, blank=False)
	description = models.TextField(default='', null=True, blank=True)
	mindate = ApproximateDateField(null=True, blank=True)
	maxdate = ApproximateDateField(null=True, blank=True)
	presentation = models.FileField(upload_to="presentations/%Y_%m_%d_%h_%M_%s", default='', null=False, blank=False)
	presentation_text = models.TextField(default='', null=True, blank=True)
	extracted = models.BooleanField(default=False)
	tags = TaggableManager(blank=True)

	def getSlideOne(self):
		"""
		   Get the first slide image of a lecture  
		"""
		x = lectureSlides.objects.filter(lecture=self.pk, slide_number=0)[:1]
		y = x[0].slide
		return x[0].slide

	def __unicode__(self):
		return self.title


# lecture segments
class lectureSegments(models.Model):
	lecture = models.ForeignKey(lectures, related_name='lectureSegments')
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	description = models.TextField(default='', null=True, blank=True)
	mindate = ApproximateDateField(null=True, blank=True)
	maxdate = ApproximateDateField(null=True, blank=True)
	minslidenumber = models.IntegerField(default=0, null=False, blank=False)
	maxslidenumber = models.IntegerField(default=0, null=False, blank=False)
	presentation = models.FileField(upload_to="presentations/%Y_%m_%d_%h_%M_%s", default='', null=False, blank=False)
	presentation_text = models.TextField(default='', null=True, blank=True)
	extracted = models.BooleanField(default=False)
	updated_lecture_review = models.BooleanField(default=False)
	tags = TaggableManager(blank=True)

	def getSlideOne(self):
		"""
		   Get the first slide image of a lecture  
		"""
		x = lectureSlidesSegment.objects.filter(lecture_segment=self.pk, slide_number=0)[:1]
		y = x[0].slide
		return x[0].slide


# lecture documents
class lectureDocuments(models.Model):
	lecture = models.ForeignKey(lectures, related_name='lectureDocsLecture')
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	description = models.TextField(default='', null=True, blank=True)
	document = models.FileField(upload_to="presentation_docs/%Y_%m_%d_%h_%M_%s", default='', null=False, blank=False)
	document_contents = models.TextField(default='', null=True, blank=True)
	extracted = models.BooleanField(default=False)
	tags = TaggableManager(blank=True)


# lecture slides
class lectureSlides(models.Model):
	lecture = models.ForeignKey(lectures, related_name='lectureSlidesLecture')
	created = models.DateTimeField(auto_now_add=True)
	presentation = models.FileField(upload_to="presentation_slides/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	slide = models.ImageField(upload_to="presentation_slides/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	slide_number = models.IntegerField(default=0, null=True, blank=True)
	slide_main_text = models.TextField(default='', null=True, blank=True)
	slide_notes = models.TextField(default='', null=True, blank=True)
	slide_notes_document = models.FileField(upload_to="slide_notes_docs/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	extracted = models.BooleanField(default=False)
	tags = TaggableManager(blank=True)

# lecture slides
class lectureSlidesSegment(models.Model):
	lecture_segment = models.ForeignKey(lectureSegments, related_name='lectureSlidesLectureSegment')
	created = models.DateTimeField(auto_now_add=True)
	slide = models.ImageField(upload_to="presentation_slides/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	slide_number = models.IntegerField(default=0, null=True, blank=True)
	extracted = models.BooleanField(default=False)

#bundles
class bundles(models.Model):
	# Links bundle to a User model instance.
	user = models.ForeignKey(User)
	title = models.CharField(max_length=255, null=False, blank=False)

#modules in bundle
class bundleModule(models.Model):
	bundle = models.ForeignKey(bundles)
	module = models.ForeignKey(modules)

#lectures in bundle
class bundleLecture(models.Model):
	bundle = models.ForeignKey(bundles)
	lecture = models.ForeignKey(lectures)

#lectureSegments in bundle
class bundleLectureSegments(models.Model):
	bundle = models.ForeignKey(bundles)
	lectureSegment = models.ForeignKey(lectureSegments)

#lectureDocuments in bundle
class bundleLectureDocument(models.Model):
	bundle = models.ForeignKey(bundles)
	lectureDocument = models.ForeignKey(lectureDocuments)

#lectureSlides in bundle
class bundleLectureSlides(models.Model):
	bundle = models.ForeignKey(bundles)
	lectureSlide = models.ForeignKey(lectureSlides)

#saved Searches
class savedSearches(models.Model):
	# Links bundle to a User model instance.
	user = models.ForeignKey(User)
	searchString = models.CharField(max_length=255, null=False, blank=False)

#comments
# Comments on Media Audio
class modulesComments(models.Model): 
    user = models.ForeignKey(User)    
    module = models.ForeignKey(modules)
    comment = models.CharField(max_length=2000, null=False, blank=False)    
    created = models.DateTimeField(auto_now_add=True)
           
    def __unicode__(self):
        return self.comment

class lecturesComments(models.Model): 
    user = models.ForeignKey(User)    
    lecture = models.ForeignKey(lectures)
    comment = models.CharField(max_length=2000, null=False, blank=False)    
    created = models.DateTimeField(auto_now_add=True)
           
    def __unicode__(self):
        return self.comment

class lectureSegmentsComments(models.Model): 
    user = models.ForeignKey(User)    
    lectureSegment = models.ForeignKey(lectureSegments)
    comment = models.CharField(max_length=2000, null=False, blank=False)    
    created = models.DateTimeField(auto_now_add=True)
           
    def __unicode__(self):
        return self.comment

class lectureDocumentsComments(models.Model): 
    user = models.ForeignKey(User)    
    lectureDocument = models.ForeignKey(lectureDocuments)
    comment = models.CharField(max_length=2000, null=False, blank=False)    
    created = models.DateTimeField(auto_now_add=True)
           
    def __unicode__(self):
        return self.comment

class lectureSlidesComments(models.Model): 
    user = models.ForeignKey(User)    
    lectureSlide = models.ForeignKey(lectureSlides)
    comment = models.CharField(max_length=2000, null=False, blank=False)    
    created = models.DateTimeField(auto_now_add=True)
           
    def __unicode__(self):
        return self.comment

