from django.db import models

# import User model
from django.contrib.auth.models import User

# course modules
class modules(models.Model):
	created = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	authors = models.CharField(max_length=255, default='', null=False, blank=False)

	def __unicode__(self):
		return self.title

#module documents
class moduleDocuments(models.Model):
	module = models.ForeignKey(modules, related_name='moduleDocsModule')
	created = models.DateTimeField(auto_now=True)
	document = models.FileField(upload_to="module_docs/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	document_contents = models.TextField(default='', null=True, blank=True)

# lectures
class lectures(models.Model):
	module = models.ForeignKey(modules, related_name='lecturesModule')
	created = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	authors = models.CharField(max_length=255, default='', null=False, blank=False)
	presentation = models.FileField(upload_to="presentations/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	presentation_text = models.TextField(default='', null=True, blank=True)
	extracted = models.BooleanField(default=False)

	def getSlideOne(self):
		"""
		   Get the first slide image of a lecture  
		"""
		x = lectureSlides.objects.filter(lecture=self.pk, slide_number=0)[:1]
		y = x[0].slide
		return x[0].slide

	def __unicode__(self):
		return self.title

# lecture documents
class lectureDocuments(models.Model):
	lecture = models.ForeignKey(lectures, related_name='lectureDocsLecture')
	created = models.DateTimeField(auto_now=True)
	document = models.FileField(upload_to="presentation_docs/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	document_contents = models.TextField(default='', null=True, blank=True)

# lecture slides
class lectureSlides(models.Model):
	lecture = models.ForeignKey(lectures, related_name='lectureSlidesLecture')
	created = models.DateTimeField(auto_now=True)
	slide = models.ImageField(upload_to="presentation_slides/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	slide_number = models.IntegerField(default=0, null=True, blank=True)
	slide_main_text = models.TextField(default='', null=True, blank=True)
	slide_notes = models.TextField(default='', null=True, blank=True)
	slide_notes_document = models.FileField(upload_to="slide_notes_docs/%Y_%m_%d_%h_%M_%s", null=True, blank=True)


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

#lectureDocuments in bundle
class bundleLectureDocument(models.Model):
	bundle = models.ForeignKey(bundles)
	lectureDocument = models.ForeignKey(lectureDocuments)

#lectureSlides in bundle
class bundleLectureSlides(models.Model):
	bundle = models.ForeignKey(bundles)
	lectureSlide = models.ForeignKey(lectureSlides)

