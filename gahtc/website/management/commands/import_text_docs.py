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
        moduleDocumentsObjects = moduleDocuments.objects.filter(extracted=False)
        exclude = set(string.punctuation)

        # loop through modules and pull all text
        for moduleDocumentsObject in moduleDocumentsObjects:
            if moduleDocumentsObject.document:
                print moduleDocumentsObject.document
                try:
                    path_to_file = MEDIA_ROOT + '/' + str(moduleDocumentsObject.document)
                    document_contents = textract.process(path_to_file, encoding='ascii')

                    # save this string for free text search
                    moduleDocumentsObject.document_contents = document_contents

                    moduleDocumentsObject.extracted = True
                    moduleDocumentsObject.save()

                except Exception as e:
                    # email admins with an alert of the problem
                    group = models.Group.objects.get(name="superusers")
                    users = group.user_set.all()
                    useremails = []
                    for u in users:
                        useremails.append(u.email)

                    subject = "[GAHTC] There was an error importing contents of a module document."
                    html_message = "Hello!<br /><br />There was an error importing contents of a module document located here:<br /><br />"+ str(moduleDocumentsObject.document) + "<br /><br />Please log in to the <a href='http://gahtc.org/dashboard/'>admin area</a> and review this file for any obvious problems. These may include files that are not .doc, .docx, or PDF files, or empty documents. If you're unable to diagnose the problem, please contact JD Godchaux at jd@nijel.org.<br /><br />Thank you!<br />GAHTC | Global Architectural History Teaching Collaborative<br /><br />Error message:" + str(e)
                    message = "Hello! There was an error importing contents of a module document located here: "+ str(moduleDocumentsObject.document) + ". Please log in to the admin area: http://gahtc.org/dashboard/ and review this file for any obvious problems. These may include files that are not .doc, .docx, or PDF files, or empty documents. If you're unable to diagnose the problem, please contact JD Godchaux at jd@nijel.org. Thank you! GAHTC | Global Architectural History Teaching Collaborative. Error message:" + str(e)

                    print e

                    send_mail(subject, message, 'gahtcweb@gmail.com', useremails, fail_silently=True, html_message=html_message)

                    pass


    def extract_text_from_lectureDocuments(self):
        # pull files from database
        lectureDocumentsObjects = lectureDocuments.objects.filter(extracted=False)

        # loop through modules and pull all text
        for lectureDocumentsObject in lectureDocumentsObjects:
            if lectureDocumentsObject.document:
                print lectureDocumentsObject.document
                try:
                    path_to_file = MEDIA_ROOT + '/' + str(lectureDocumentsObject.document)
                    document_contents = textract.process(path_to_file, encoding='ascii')

                    # save this string
                    lectureDocumentsObject.document_contents = document_contents
                    lectureDocumentsObject.extracted = True
                    lectureDocumentsObject.save()

                except Exception as e:
                    # email admins with an alert of the problem
                    group = models.Group.objects.get(name="superusers")
                    users = group.user_set.all()
                    useremails = []
                    for u in users:
                        useremails.append(u.email)

                    subject = "[GAHTC] There was an error importing contents of a lecture document."
                    html_message = "Hello!<br /><br />There was an error importing contents of a module document located here:<br /><br />"+ str(lectureDocumentsObject.document) + "<br /><br />Please log in to the <a href='http://gahtc.org/dashboard/'>admin area</a> and review this file for any obvious problems. These may include files that are not .doc, .docx, or PDF files, or empty documents. If you're unable to diagnose the problem, please contact JD Godchaux at jd@nijel.org.<br /><br />Thank you!<br />GAHTC | Global Architectural History Teaching Collaborative<br /><br />Error message:" + str(e)
                    message = "Hello! There was an error importing contents of a module document located here: "+ str(lectureDocumentsObject.document) + ". Please log in to the admin area: http://gahtc.org/dashboard/ and review this file for any obvious problems. These may include files that are not .doc, .docx, or PDF files, or empty documents. If you're unable to diagnose the problem, please contact JD Godchaux at jd@nijel.org. Thank you! GAHTC | Global Architectural History Teaching Collaborative. Error message:" + str(e)

                    print e

                    send_mail(subject, message, 'gahtcweb@gmail.com', useremails, fail_silently=True, html_message=html_message)

                    pass                


    def handle(self, *args, **options):
        print "Extracting text from moduleDocuments...."
        self.extract_text_from_moduleDocuments()
        print "Extracting text from lectureDocuments...."
        self.extract_text_from_lectureDocuments()
        print "Done."
