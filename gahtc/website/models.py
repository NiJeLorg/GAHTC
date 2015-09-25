from django.db import models

# course modules
class modules(models.Model):
	created = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length=255, default='', null=False, blank=False)
	authors = models.CharField(max_length=255, default='', null=False, blank=False)
	syllabus = models.FileField(upload_to="module_docs/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	syllabus_contents = models.TextField(default='', null=True, blank=True)
	overview = models.FileField(upload_to="module_docs/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	overview_contents = models.TextField(default='', null=True, blank=True)

	def __unicode__(self):
		return self.title

# lectures
class lectures(models.Model):
	module = models.ForeignKey(modules)
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
	lecture = models.ForeignKey(lectures)
	created = models.DateTimeField(auto_now=True)
	document = models.FileField(upload_to="presentation_docs/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	document_contents = models.TextField(default='', null=True, blank=True)

# lecture slides
class lectureSlides(models.Model):
	lecture = models.ForeignKey(lectures)
	created = models.DateTimeField(auto_now=True)
	slide = models.ImageField(upload_to="presentation_slides/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	slide_number = models.IntegerField(default=0, null=True, blank=True)
	slide_main_text = models.TextField(default='', null=True, blank=True)
	slide_notes = models.TextField(default='', null=True, blank=True)
