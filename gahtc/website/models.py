from django.db import models

# import User model
from django.contrib.auth.models import User

# django taggit import
from taggit_autosuggest.managers import TaggableManager

# import ApproximateDateField
from django_date_extensions.fields import ApproximateDateField

# user profile
class profile(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=255, default='', null=False, blank=False)
	institution = models.CharField(max_length=255, default='', null=False, blank=False)
	teaching = models.TextField(default='', null=False, blank=False)
	introduction = models.TextField(default='', null=False, blank=False)
	pic = models.ImageField(upload_to="bio_pics/%Y_%m_%d_%h_%M_%s", null=True, blank=True)

	def __unicode__(self):
		return self.name

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
	document = models.FileField(upload_to="module_docs/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
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
	presentation = models.FileField(upload_to="presentations/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
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
	presentation = models.FileField(upload_to="presentations/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	presentation_text = models.TextField(default='', null=True, blank=True)
	extracted = models.BooleanField(default=False)
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
	document = models.FileField(upload_to="presentation_docs/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	document_contents = models.TextField(default='', null=True, blank=True)
	extracted = models.BooleanField(default=False)
	tags = TaggableManager(blank=True)


# lecture slides
class lectureSlides(models.Model):
	lecture = models.ForeignKey(lectures, related_name='lectureSlidesLecture')
	created = models.DateTimeField(auto_now_add=True)
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

