from django.db import models

# course modules
class modules(models.Model):
	created = models.DateTimeField(auto_now=True)
	syllabus = models.FileField(upload_to="module_docs/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	syllabus_contents = models.TextField(default='', null=True, blank=True)
	overview = models.FileField(upload_to="module_docs/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
	overview_contents = models.TextField(default='', null=True, blank=True)

# lectures
class lectures(models.Model):
	module = models.ForeignKey(modules)
	created = models.DateTimeField(auto_now=True)
	presentation = models.FileField(upload_to="presentations/%Y_%m_%d_%h_%M_%s", null=True, blank=True)

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
	slide_notes = models.TextField(default='', null=True, blank=True)