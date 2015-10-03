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

    def extract_text_from_moduleDocuments(self):
        # pull files from database
        moduleDocumentsObjects = moduleDocuments.objects.all()

        # loop through modules and pull all text
        for moduleDocumentsObject in moduleDocumentsObjects:
            if moduleDocumentsObject.document:
                print moduleDocumentsObject.document
                path_to_file = MEDIA_ROOT + '/' + str(moduleDocumentsObject.document)
                document_contents = textract.process(path_to_file)

                # save this string
                moduleDocumentsObject.document_contents = strip_non_ascii(document_contents)
                moduleDocumentsObject.save()

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
        print "Extracting text from moduleDocuments...."
        self.extract_text_from_moduleDocuments()
        print "Extracting text from lectureDocuments...."
        self.extract_text_from_lectureDocuments()
        print "Done."





