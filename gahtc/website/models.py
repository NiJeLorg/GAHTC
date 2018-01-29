from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

# import User model
from django.contrib.auth.models import User

# django taggit import
from taggit_autosuggest.managers import TaggableManager

#wagtail imports
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

# #thumbnails using imagekit
# from imagekit import ImageSpec, register
# from imagekit.processors import ResizeToFill


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
	first_name = models.CharField(max_length=255, default='', null=False, blank=False)
	last_name = models.CharField(max_length=255, default='', null=False, blank=False)
	name = models.CharField(max_length=255, default='', null=False, blank=False)
	institution = models.CharField(max_length=255, default='', null=False, blank=False)
	institution_address = models.CharField(max_length=255, default='', null=True, blank=True)
	institution_city = models.CharField(max_length=255, default='', null=True, blank=True)
	institution_country = models.CharField(max_length=255, default='', null=True, blank=True)
	institution_postal_code = models.CharField(max_length=255, default='', null=True, blank=True)
	teaching = models.TextField(default='', null=False, blank=False)
	introduction = models.TextField(default='', null=False, blank=False)
	avatar = models.ImageField(upload_to="bio_pics/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	website = models.URLField(max_length=255, default='', null=True, blank=True)
	instutution_document = models.FileField(upload_to="insitution_docs/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	verified = models.NullBooleanField(default=None)
	public = models.BooleanField(default=True)

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name


# course modules
class modules(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	authors = models.CharField(max_length=255, default='', null=False, blank=False)
	authors_m2m = models.ManyToManyField(profile)
	description = models.TextField(default='', null=True, blank=True)
	keywords = TaggableManager(blank=True)
	cover_image = models.ImageField(upload_to="module_cover/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	featured = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.title

#document types lookup
class docType(models.Model):
	name = models.CharField(max_length=255, default='', null=False, blank=False)

	def __unicode__(self):
		return self.name

#module documents
class moduleDocuments(models.Model):
	module = models.ForeignKey(modules, related_name='moduleDocsModule')
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	description = models.TextField(default='', null=True, blank=True)
	document = models.FileField(upload_to="module_docs/%Y_%m_%d_%h_%M_%s", default='', null=False, blank=False)
	document_contents = models.TextField(default='', null=True, blank=True)
	extracted = models.BooleanField(default=False)
	keywords = TaggableManager(blank=True)
	doc_type = models.ForeignKey(docType, related_name='module_doc_type', null=True, blank=True, default='', on_delete=models.SET_NULL)

# lectures
class lectures(models.Model):
	module = models.ForeignKey(modules, related_name='lecturesModule')
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	authors = models.CharField(max_length=255, default='', null=False, blank=False)
	authors_m2m = models.ManyToManyField(profile)
	description = models.TextField(default='', null=True, blank=True)
	presentation = models.FileField(upload_to="presentations/%Y_%m_%d_%h_%M_%s", default='', null=False, blank=False)
	presentation_text = models.TextField(default='', null=True, blank=True)
	extracted = models.BooleanField(default=False)
	keywords = TaggableManager(blank=True)

	def getSlideOne(self):
		"""
		   Get the first slide image of a lecture  
		"""
		x = lectureSlides.objects.filter(lecture=self.pk, slide_number=0)[:1]
		try:
			y = x[0].slide
		except Exception as e:
			y = None
		
		return y

	def __unicode__(self):
		return self.title


# lecture segments
class lectureSegments(models.Model):
	lecture = models.ForeignKey(lectures, related_name='lectureSegments')
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	description = models.TextField(default='', null=True, blank=True)
	minslidenumber = models.IntegerField(default=0, null=False, blank=False)
	maxslidenumber = models.IntegerField(default=0, null=False, blank=False)
	presentation = models.FileField(upload_to="presentations/%Y_%m_%d_%h_%M_%s", default='', null=False, blank=False)
	presentation_text = models.TextField(default='', null=True, blank=True)
	extracted = models.BooleanField(default=False)
	updated_lecture_review = models.BooleanField(default=False)
	keywords = TaggableManager(blank=True)

	def getSlideOne(self):
		"""
		   Get the first slide image of a lecture  
		"""
		x = lectureSlidesSegment.objects.filter(lecture_segment=self.pk, slide_number=0)[:1]
		try:
			y = x[0].slide
		except Exception as e:
			y = None
		
		return y

# lecture documents
class lectureDocuments(models.Model):
	lecture = models.ForeignKey(lectures, related_name='lectureDocsLecture')
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	description = models.TextField(default='', null=True, blank=True)
	document = models.FileField(upload_to="presentation_docs/%Y_%m_%d_%h_%M_%s", default='', null=False, blank=False)
	document_contents = models.TextField(default='', null=True, blank=True)
	extracted = models.BooleanField(default=False)
	keywords = TaggableManager(blank=True)
	doc_type = models.ForeignKey(docType, related_name='lecture_doc_type', null=True, blank=True, default='', on_delete=models.SET_NULL)


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
	keywords = TaggableManager(blank=True)

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
	contact = models.BooleanField(default=False)
	downloaded = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

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

# storing download and contact data for modules and lectures
class userModuleDownload(models.Model):
	user = models.ForeignKey(User)
	module = models.ForeignKey(modules)
	contact = models.BooleanField(default=False)
	downloaded = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

class userLectureDownload(models.Model):
	user = models.ForeignKey(User)
	lecture = models.ForeignKey(lectures)
	contact = models.BooleanField(default=False)
	downloaded = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)	
	
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

# coming soon course modules
class comingSoonModules(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	authors = models.CharField(max_length=255, default='', null=False, blank=False)
	authors_m2m = models.ManyToManyField(profile)
	description = models.TextField(default='', null=True, blank=True)
	cover_image = models.ImageField(upload_to="module_cover/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	keywords = TaggableManager(blank=True)

	def __unicode__(self):
		return self.title



#wagtail CMS models
class TextHeavyPages(Page):
	# Database fields
	date = models.DateField("Updated On")
	splash_image = models.ForeignKey(
		'wagtailimages.Image',
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)
	page_content = RichTextField(blank=True)

	search_fields = Page.search_fields + [
		index.SearchField('page_content'),
		index.FilterField('date'),
	]

	# Editor panels configuration
	content_panels = Page.content_panels + [
		ImageChooserPanel('splash_image'),
		FieldPanel('page_content', classname="full"),
		FieldPanel('date')
	]

# #thumbnail imagekit generator
# class Thumbnail(ImageSpec):
#     processors = [ResizeToFill(400, 250)]
#     format = 'JPEG'
#     options = {'quality': 90}

# register.generator('website:thumbnail', Thumbnail)

#wagtail snippet model for sidebar content
@register_snippet
@python_2_unicode_compatible  # provide equivalent __unicode__ and __str__ methods on Python 2
class sidebarContent(models.Model):
	header = models.CharField(max_length=255, default='', null=False, blank=False)
	text = RichTextField(blank=True)
	
	panels = [
		FieldPanel('header'),
        FieldPanel('text', classname="full"),
    ]
	
	def __str__(self):
		return self.header