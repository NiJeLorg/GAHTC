from django.contrib import admin

# Register your models here.
from website.models import *

admin.site.register(modules)
admin.site.register(moduleDocuments)
admin.site.register(lectures)
admin.site.register(lectureDocuments)
admin.site.register(lectureSlides)
admin.site.register(bundles)
admin.site.register(bundleModule)
admin.site.register(bundleLecture)
admin.site.register(bundleLectureDocument)
admin.site.register(bundleLectureSlides)
admin.site.register(profile)
