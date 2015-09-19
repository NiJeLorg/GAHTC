import sys,os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from website.models import *
import textract

"""
  Opens files and extracts all text
"""
# path to media root for textract to find files
MEDIA_ROOT = settings.MEDIA_ROOT

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if ord(c) >= 32 or ord(c) <= 126)
    return ''.join(stripped)


class Command(BaseCommand):

    def extract_text_from_syllabus(self):
        # pull files from database
        modulesObjects = modules.objects.all()

        # loop through modules and pull all text
        for modulesObject in modulesObjects:
            if modulesObject.syllabus:
                print modulesObject.syllabus
                path_to_file = MEDIA_ROOT + '/' + str(modulesObject.syllabus)
                syllabus_contents = textract.process(path_to_file)

                # save this string
                modulesObject.syllabus_contents = strip_non_ascii(syllabus_contents)
                modulesObject.save()

    def extract_text_from_overview(self):
        # pull files from database
        modulesObjects = modules.objects.all()

        # loop through modules and pull all text
        for modulesObject in modulesObjects:
            if modulesObject.overview:
                print modulesObject.overview
                path_to_file = MEDIA_ROOT + '/' + str(modulesObject.overview)
                overview_contents = textract.process(path_to_file)

                # save this string
                modulesObject.overview_contents = strip_non_ascii(overview_contents)
                modulesObject.save()

    def extract_text_from_lectureDocuments(self):
        # pull files from database
        lectureDocumentsObjects = lectureDocuments.objects.all()

        # loop through modules and pull all text
        for lectureDocumentsObject in lectureDocumentsObjects:
            if lectureDocumentsObject.document:
                print lectureDocumentsObject.document
                path_to_file = MEDIA_ROOT + '/' + str(lectureDocumentsObject.document)
                document_contents = textract.process(path_to_file)

                # save this string
                lectureDocumentsObject.document_contents = strip_non_ascii(document_contents)
                lectureDocumentsObject.save()


    def handle(self, *args, **options):
        print "Extracting text from syllabus...."
        self.extract_text_from_syllabus()
        print "Extracting text from overview...."
        self.extract_text_from_overview()
        print "Extracting text from lectureDocuments...."
        self.extract_text_from_lectureDocuments()
        print "Done."





