import sys,os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from website.models import *
import textract
import string
from textblob import TextBlob

"""
  Opens files and extracts all text
"""
# path to media root for textract to find files
MEDIA_ROOT = settings.MEDIA_ROOT
exclude = set(string.punctuation)

class Command(BaseCommand):

    def extract_text_from_moduleDocuments(self):
        # pull files from database
        moduleDocumentsObjects = moduleDocuments.objects.all()
        exclude = set(string.punctuation)

        # loop through modules and pull all text
        for moduleDocumentsObject in moduleDocumentsObjects:
            if moduleDocumentsObject.document:
                print moduleDocumentsObject.document
                path_to_file = MEDIA_ROOT + '/' + str(moduleDocumentsObject.document)
                document_contents = textract.process(path_to_file, encoding='ascii')

                # create tags from noun_phrases
                # only add tags if none exist
                if not moduleDocumentsObject.tags:
                    blobbed = TextBlob(document_contents)
                    np = blobbed.noun_phrases
                    np = list(set(np))
                    np = [s for s in np if s]
                    moduleDocumentsObject.tags.clear()
                    for item in np:
                        s = ''.join(ch for ch in item if ch not in exclude)
                        moduleDocumentsObject.tags.add(s)

                # TODO pull dates
                # words = blobbed.words
                # print words
                # numbers = []
                # for w in words:
                #     try:
                #         int(w)
                #         numbers.append(int(w))
                #     except ValueError:
                #         pass

                # print numbers
                # numbers_not_single_digits =  [x for x in numbers if not 0 <= x <= 20]
                # print numbers_not_single_digits
                # numbers_pub_dates = [x for x in numbers_not_single_digits if not 0 <= x <= 2020]
                # print numbers_pub_dates
                #end TODO


                # save this string for free text search
                moduleDocumentsObject.document_contents = document_contents

                moduleDocumentsObject.extracted = True
                moduleDocumentsObject.save()

    def extract_text_from_lectureDocuments(self):
        # pull files from database
        lectureDocumentsObjects = lectureDocuments.objects.filter(extracted=False)

        # loop through modules and pull all text
        for lectureDocumentsObject in lectureDocumentsObjects:
            if lectureDocumentsObject.document:
                print lectureDocumentsObject.document
                path_to_file = MEDIA_ROOT + '/' + str(lectureDocumentsObject.document)
                document_contents = textract.process(path_to_file, encoding='ascii')

                # create tags from noun_phrases
                # only add tags if none exist
                if not lectureDocumentsObject.tags:
                    blobbed = TextBlob(document_contents)
                    np = blobbed.noun_phrases
                    np = list(set(np))
                    np = [s for s in np if s]
                    lectureDocumentsObject.tags.clear()
                    for item in np:
                        s = ''.join(ch for ch in item if ch not in exclude)
                        lectureDocumentsObject.tags.add(s)

                # save this string
                lectureDocumentsObject.document_contents = document_contents
                lectureDocumentsObject.extracted = True
                lectureDocumentsObject.save()


    def handle(self, *args, **options):
        print "Extracting text from moduleDocuments...."
        self.extract_text_from_moduleDocuments()
        print "Extracting text from lectureDocuments...."
        self.extract_text_from_lectureDocuments()
        print "Done."
