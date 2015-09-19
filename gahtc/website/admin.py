from django.contrib import admin

# Register your models here.
from website.models import *

admin.site.register(modules)
admin.site.register(lectures)
admin.site.register(lectureDocuments)
admin.site.register(lectureSlides)
